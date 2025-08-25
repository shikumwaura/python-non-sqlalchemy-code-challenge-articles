class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author name must be a non-empty string")
        object.__setattr__(self, '_name', name)

    def __setattr__(self, key, value):
        if key == 'name' and hasattr(self, '_name'):
            # silently ignore attempts to change name (immutable)
            return
        object.__setattr__(self, key, value)

    @property
    def name(self):
        return self._name

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
    # Simply create the Article (which auto-appends in __init__)
      article = Article(self, magazine, title)
      return article


    def topic_areas(self):
        mags = self.magazines()
        if not mags:
            return None
        return list({mag.category for mag in mags})


class Magazine:
    _all_magazines = []

    def __init__(self, name, category):
        self._name = None
        self._category = None
        self.name = name
        self.category = category
        Magazine._all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not 2 <= len(value) <= 16:
            return  # silently ignore invalid
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            return  # silently ignore invalid
        self._category = value

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        arts = self.articles()
        if not arts:
            return None
        return [article.title for article in arts]

    def contributing_authors(self):
        authors = self.contributors()
        contributors = [author for author in authors if sum(
            1 for article in Article.all if article.magazine == self and article.author == author) > 2]
        return contributors if contributors else None

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        counts = {}
        for article in Article.all:
            counts[article.magazine] = counts.get(article.magazine, 0) + 1
        top_mag = max(counts, key=counts.get)
        return top_mag


class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise TypeError("author must be Author instance")
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be Magazine instance")
        if not isinstance(title, str) or not 5 <= len(title) <= 50:
            raise ValueError("title must be string 5-50 chars")
        self.author = author
        self.magazine = magazine
        object.__setattr__(self, '_title', title)
        Article.all.append(self)

    def __setattr__(self, key, value):
        # silently ignore attempts to set title after creation
        if key == 'title' and hasattr(self, '_title'):
            return
        object.__setattr__(self, key, value)

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError("author must be Author instance")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise TypeError("magazine must be Magazine instance")
        self._magazine = value
