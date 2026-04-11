<?php
/**
 * API configuration.
 *
 * Set environment variables to override defaults:
 *   FRONTEND_ORIGIN  — full origin of the WordPress site, e.g. https://example.com
 *   API_KEY          — shared secret clients send in X-Api-Key header; leave empty to disable
 *   PYTHON_BIN       — path to the Python 3 interpreter (default: python3)
 *   OPENWEATHER_API_KEY — forwarded to the Python script as an env var
 */
declare(strict_types=1);

return [

    // -----------------------------------------------------------------
    // CORS
    // -----------------------------------------------------------------
    // List every origin that is allowed to call this API.
    // Requests from unlisted origins will not receive CORS credentials.
    'allowed_origins' => array_filter([
        getenv('FRONTEND_ORIGIN') ?: 'https://example.com',
    ]),

    // -----------------------------------------------------------------
    // API key protection  (optional)
    // -----------------------------------------------------------------
    // If non-empty, every request must include the matching value in the
    // X-Api-Key header.  Set to '' to disable.
    'api_key' => (string)(getenv('API_KEY') ?: ''),

    // -----------------------------------------------------------------
    // Rate limiting  (file-based, per-IP, per-minute)
    // -----------------------------------------------------------------
    'rate_limit' => [
        'enabled'             => true,
        'requests_per_minute' => 60,
        // Writable directory for counter files.  Created automatically.
        'storage_path'        => __DIR__ . '/rate_limit/',
    ],

    // -----------------------------------------------------------------
    // Python subprocess
    // -----------------------------------------------------------------
    'python' => [
        'executable'  => (string)(getenv('PYTHON_BIN') ?: 'python3'),
        'script'      => dirname(__DIR__) . '/src/efficiency-calculator/cli.py',
        // cwd must be the package directory so relative imports resolve.
        'working_dir' => dirname(__DIR__) . '/src/efficiency-calculator',
        // Hard timeout in seconds.  Cached runs finish in <1 s;
        // uncached runs fetch 365 API days and may take 30–60 s.
        'timeout'     => 30,
    ],
];
