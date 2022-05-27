class Category:
    """
    Category

    Attributes:
        name: Category name
        description: Category description
        created_at: Opening time
    """

    def __init__(self, data):

        # Category name
        self.name = data.get('name', '')

        # Description
        self.description = data.get('description', '')

        # Created date
        self.created_at = data.get('created_at', '')
