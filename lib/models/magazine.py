from lib.db.connection import get_connection



class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,)).fetchone()
        conn.close()
        return cls(**row) if row else None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,)).fetchone()
        conn.close()
        return cls(**row) if row else None

    def contributors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
        """, (self.id,)).fetchall()
        conn.close()
        return [Author(**row) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,)).fetchall()
        conn.close()
        return [row["title"] for row in rows]

    def contributing_authors(self):
        from lib.models.author import Author
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT authors.*, COUNT(articles.id) AS article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,)).fetchall()
        conn.close()
        return [Author(**row) for row in rows]

    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT magazines.* FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            GROUP BY magazines.id
            HAVING COUNT(DISTINCT articles.author_id) > 1
        """).fetchall()
        conn.close()
        return [cls(**row) for row in rows]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT magazines.*, COUNT(articles.id) as article_count
            FROM magazines
            LEFT JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
        """).fetchall()
        conn.close()
        return [dict(row) for row in rows]
