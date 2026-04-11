<?php
/**
 * POST /api/calculate
 *
 * Request body (JSON):
 *   {
 *     "value1": <number>,   // latitude  (-90 … 90)
 *     "value2": <number>,   // longitude (-180 … 180)
 *     "year":   <integer>,  // optional, default 2023
 *     "turbine": <string>   // optional: "STANDARD_HAWT" | "WITEROK", default "STANDARD_HAWT"
 *   }
 *
 * Success response (200):
 *   { "result": <number> }   // annual energy production in kWh
 *
 * Error responses:
 *   400 — invalid / missing input
 *   401 — bad or missing API key
 *   404 — unknown route
 *   405 — wrong HTTP method
 *   429 — rate limit exceeded
 *   500 — internal / Python error
 */
declare(strict_types=1);

$config = require __DIR__ . '/config.php';

// Always respond with JSON.
header('Content-Type: application/json; charset=utf-8');

// -------------------------------------------------------------------------
// CORS
// -------------------------------------------------------------------------
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if (in_array($origin, $config['allowed_origins'], true)) {
    header("Access-Control-Allow-Origin: $origin");
    header('Vary: Origin');
} elseif (!empty($config['allowed_origins'])) {
    // Reflect only the primary allowed origin for non-matching requests so
    // browsers see a consistent CORS header (request will still be blocked).
    header('Access-Control-Allow-Origin: ' . $config['allowed_origins'][0]);
}
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Api-Key');
header('Access-Control-Max-Age: 86400');

// Handle CORS preflight — must come before any auth checks.
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// -------------------------------------------------------------------------
// Routing
// -------------------------------------------------------------------------
$method = $_SERVER['REQUEST_METHOD'];
$path   = '/' . trim((string) parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH), '/');

if ($method !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

if ($path !== '/api/calculate') {
    http_response_code(404);
    echo json_encode(['error' => 'Not found']);
    exit;
}

// -------------------------------------------------------------------------
// API key  (optional — skipped when config value is empty)
// -------------------------------------------------------------------------
$apiKey = $config['api_key'];
if ($apiKey !== '') {
    $provided = $_SERVER['HTTP_X_API_KEY'] ?? '';
    if (!hash_equals($apiKey, $provided)) {
        http_response_code(401);
        echo json_encode(['error' => 'Unauthorized: invalid or missing X-Api-Key header']);
        exit;
    }
}

// -------------------------------------------------------------------------
// Rate limiting  (file-based, per IP, per minute)
// -------------------------------------------------------------------------
if ($config['rate_limit']['enabled']) {
    $storePath = $config['rate_limit']['storage_path'];

    if (!is_dir($storePath)) {
        mkdir($storePath, 0755, true);
    }

    // Remove counter files older than 2 minutes to keep the directory tidy.
    foreach (glob($storePath . '*.txt') ?: [] as $staleFile) {
        if (filemtime($staleFile) < time() - 120) {
            @unlink($staleFile);
        }
    }

    $ip     = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
    $bucket = (int) floor(time() / 60);                 // changes every minute
    $key    = hash('sha256', $ip) . '_' . $bucket;
    $file   = $storePath . $key . '.txt';

    $count = (int) @file_get_contents($file);

    if ($count >= $config['rate_limit']['requests_per_minute']) {
        $retryAfter = 60 - (time() % 60);
        http_response_code(429);
        header("Retry-After: $retryAfter");
        echo json_encode(['error' => "Too many requests. Retry after $retryAfter seconds."]);
        exit;
    }

    file_put_contents($file, $count + 1, LOCK_EX);
}

// -------------------------------------------------------------------------
// Parse request body
// -------------------------------------------------------------------------
$raw  = (string) file_get_contents('php://input');
$data = json_decode($raw, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON: ' . json_last_error_msg()]);
    exit;
}

if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['error' => 'Request body must be a JSON object']);
    exit;
}

// -------------------------------------------------------------------------
// Validate required fields
// -------------------------------------------------------------------------
if (!array_key_exists('value1', $data) || !array_key_exists('value2', $data)) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing required fields: value1, value2']);
    exit;
}

if (!is_numeric($data['value1']) || !is_numeric($data['value2'])) {
    http_response_code(400);
    echo json_encode(['error' => 'value1 and value2 must be numbers']);
    exit;
}

$lat = (float) $data['value1'];   // latitude
$lon = (float) $data['value2'];   // longitude

if ($lat < -90.0 || $lat > 90.0) {
    http_response_code(400);
    echo json_encode(['error' => 'value1 (latitude) must be between -90 and 90']);
    exit;
}

if ($lon < -180.0 || $lon > 180.0) {
    http_response_code(400);
    echo json_encode(['error' => 'value2 (longitude) must be between -180 and 180']);
    exit;
}

// -------------------------------------------------------------------------
// Validate optional fields
// -------------------------------------------------------------------------
$year = 2023;
if (array_key_exists('year', $data)) {
    if (!is_int($data['year'])) {
        http_response_code(400);
        echo json_encode(['error' => 'year must be an integer']);
        exit;
    }
    $year = $data['year'];
    if ($year < 2000 || $year > 2030) {
        http_response_code(400);
        echo json_encode(['error' => 'year must be between 2000 and 2030']);
        exit;
    }
}

$allowedTurbines = ['STANDARD_HAWT', 'WITEROK'];
$turbine = 'STANDARD_HAWT';
if (array_key_exists('turbine', $data)) {
    if (!is_string($data['turbine']) || !in_array($data['turbine'], $allowedTurbines, true)) {
        http_response_code(400);
        echo json_encode(['error' => 'turbine must be one of: ' . implode(', ', $allowedTurbines)]);
        exit;
    }
    $turbine = $data['turbine'];
}

// -------------------------------------------------------------------------
// Run calculation
// -------------------------------------------------------------------------
try {
    $result = runPython($lat, $lon, $year, $turbine, $config['python']);
    echo json_encode(['result' => $result]);
} catch (RuntimeException $e) {
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
}

// ==========================================================================

/**
 * Spawns the Python CLI script and returns the calculated result (kWh).
 *
 * Uses proc_open with an array command so no shell is involved and
 * arguments cannot be injected.
 *
 * @throws RuntimeException on timeout, non-zero exit, or unexpected output.
 */
function runPython(float $lat, float $lon, int $year, string $turbine, array $cfg): float
{
    // Build command as an array — no shell escaping needed.
    $cmd = [
        $cfg['executable'],
        $cfg['script'],
        '--lat',     (string) $lat,
        '--lon',     (string) $lon,
        '--year',    (string) $year,
        '--turbine', $turbine,
    ];

    $descriptors = [
        0 => ['pipe', 'r'],  // stdin  (we close it immediately)
        1 => ['pipe', 'w'],  // stdout (JSON result)
        2 => ['pipe', 'w'],  // stderr (error messages / tqdm progress)
    ];

    // Pass the OpenWeather API key through the environment.
    $env = array_merge($_ENV, [
        'OPENWEATHER_API_KEY' => (string)(getenv('OPENWEATHER_API_KEY') ?: ''),
    ]);

    $process = proc_open($cmd, $descriptors, $pipes, $cfg['working_dir'], $env);

    if (!is_resource($process)) {
        throw new RuntimeException('Failed to start Python subprocess');
    }

    fclose($pipes[0]);

    stream_set_blocking($pipes[1], false);
    stream_set_blocking($pipes[2], false);

    $stdout  = '';
    $stderr  = '';
    $timeout = (float) $cfg['timeout'];
    $start   = microtime(true);

    while (true) {
        $stdout .= (string) stream_get_contents($pipes[1]);
        $stderr .= (string) stream_get_contents($pipes[2]);

        $status = proc_get_status($process);
        if (!$status['running']) {
            break;
        }

        if ((microtime(true) - $start) > $timeout) {
            proc_terminate($process, 9);
            fclose($pipes[1]);
            fclose($pipes[2]);
            proc_close($process);
            throw new RuntimeException(
                sprintf('Python process timed out after %d seconds', (int) $timeout)
            );
        }

        usleep(10_000); // 10 ms polling interval
    }

    // Drain any remaining data after the process exits.
    $stdout .= (string) stream_get_contents($pipes[1]);
    $stderr .= (string) stream_get_contents($pipes[2]);

    fclose($pipes[1]);
    fclose($pipes[2]);
    $exitCode = proc_close($process);

    if ($exitCode !== 0) {
        // The Python CLI writes {"error": "..."} to stderr on failure.
        $errMsg = trim($stderr) ?: 'Unknown error (exit code ' . $exitCode . ')';
        $errData = json_decode($errMsg, true);
        if (is_array($errData) && isset($errData['error'])) {
            $errMsg = (string) $errData['error'];
        }
        throw new RuntimeException($errMsg);
    }

    $output  = trim($stdout);
    $decoded = json_decode($output, true);

    if (json_last_error() !== JSON_ERROR_NONE || !isset($decoded['result'])) {
        throw new RuntimeException('Unexpected output from calculation engine: ' . $output);
    }

    return (float) $decoded['result'];
}
