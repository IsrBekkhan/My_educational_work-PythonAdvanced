"""
Add new column to product
"""

from yoyo import step

__depends__ = {}

steps = [
    step("ALTER TABLE products ADD COLUMN color VARCHAR(100)", "ALTER TABLE products DROP COLUMN color")
]
