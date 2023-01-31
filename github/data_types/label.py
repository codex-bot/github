from data_types.user import User


class Label:
    """
    GitHub Label

    https://developer.github.com/v3/labels/

    Attributes:
        id: Label id
        node_id: Node id
        url: API URL for the label
        name: The name of the label
        description: Label description text
        color: 6-character hex code, without the leading #, identifying the color
        is_default: boolean whether this label is default
    """

    def __init__(self, data):

        # Internal GitHub id
        self.id = data.get('id', 0)
        self.node_id = data.get('node_id', 0)

        # Name and Description
        self.name = data.get('name', '')
        self.description = data.get('description', '')

        # Public link
        self.url = data.get('url', '')

        # Label color
        self.color = data.get('color', '')

        # Is default
        self.is_default = bool(data.get('default', ''))
