from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def seed():
    alice = Author(name="Alice")
    bob = Author(name="Bob")
    alice.save()
    bob.save()

    tech = Magazine(name="Tech Times", category="Technology")
    health = Magazine(name="Health Weekly", category="Health")
    tech.save()
    health.save()

    Article(title="AI Revolution", author_id=alice.id, magazine_id=tech.id).save()
    Article(title="Future of Health", author_id=alice.id, magazine_id=health.id).save()
    Article(title="Cybersecurity Tips", author_id=bob.id, magazine_id=tech.id).save()

if __name__ == "__main__":
    seed()
