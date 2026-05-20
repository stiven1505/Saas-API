-- SQL script to seed the database

-- Insert a test user with a predefined ID and hashed password ('password123')
INSERT INTO users (id, email, full_name, hashed_password, is_active, created_at, updated_at) 
VALUES ('u-1000', 'test@example.com', 'Test User', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQqiRQYq', true, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Insert Workspace Alpha
INSERT INTO workspaces (id, name, description, owner_id, is_active, created_at, updated_at) 
VALUES ('w-alpha', 'Workspace Alpha', 'Alpha workspace description', 'u-1000', true, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Insert Workspace Beta
INSERT INTO workspaces (id, name, description, owner_id, is_active, created_at, updated_at) 
VALUES ('w-beta', 'Workspace Beta', 'Beta workspace description', 'u-1000', true, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Insert Workspace Mega
INSERT INTO workspaces (id, name, description, owner_id, is_active, created_at, updated_at)
VALUES ('w-mega', 'Workspace Mega', 'Mega workspace description', 'u-1000', true, NOW(), NOW());

-- User ADMIN in Mega
INSERT INTO workspace_members (id, workspace_id, user_id, role, is_active, joined_at, updated_at)
VALUES ('wm-mega-1', 'w-mega', 'u-1000', 'READER', true, NOW(), NOW());

-- User ADMIN in Alpha
INSERT INTO workspace_members (id, workspace_id, user_id, role, is_active, joined_at, updated_at) 
VALUES ('wm-alpha-1', 'w-alpha', 'u-1000', 'ADMIN', true, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- User READER in Beta
INSERT INTO workspace_members (id, workspace_id, user_id, role, is_active, joined_at, updated_at) 
VALUES ('wm-beta-1', 'w-beta', 'u-1000', 'EDITOR', true, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Example Project in Alpha
INSERT INTO projects (id, workspace_id, name, description, status, created_by, is_active, created_at, updated_at) 
VALUES ('p-alpha-1', 'w-alpha', 'Project Phoenix', 'A top secret AI initiative.', 'ACTIVE', 'u-1000', true, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Example Project in Beta
INSERT INTO projects (id, workspace_id, name, description, status, created_by, is_active, created_at, updated_at) 
VALUES ('p-beta-1', 'w-beta', 'Project Titan', 'An outdated internal tool.', 'ON_HOLD', 'u-1000', true, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;
