CREATE TABLE IF NOT EXISTS queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_query TEXT NOT NULL,
    bot_response TEXT,
    status TEXT DEFAULT 'open',   -- 'open' for unresolved, 'closed' for resolved
    support_response TEXT         -- Staff member's response if unresolved
);

CREATE TABLE IF NOT EXISTS solutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);
