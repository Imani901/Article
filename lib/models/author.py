from lib.db.connection import get_connection



class Author:
    def __init__(self, id=None, name=None, article_count=None):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM authors WHERE name = ?", (name,)).fetchone()
        conn.close()
        return cls(id=row["id"], name=row["name"]) if row else None

    def articles(self):
        from lib.models.article import Article
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,)).fetchall()
        conn.close()
        return [Article(**row) for row in rows]
    
    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT authors.*, COUNT(articles.id) AS article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            GROUP BY authors.id
            ORDER BY article_count DESC
            LIMIT 1
        """
        row = cursor.execute(query).fetchone()
        conn.close()
        if row:
            author_data = dict(row)
            article_count = author_data.pop('article_count', None)
            author = cls(**author_data)
            author.article_count = article_count  # Attach as attribute
            return author
        return None



    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
        """, (self.id,)).fetchall()
        conn.close()
        from lib.models.magazine import Magazine
        return [Magazine(**row) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
