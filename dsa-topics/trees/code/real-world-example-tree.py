class TreeNode:
    def __init__(self, data):
        self.data = data  # Data stored in the node
        self.children = []  # List of child nodes

    def add_child(self, child_node):
        self.children.append(child_node)  # Add a child node to the current node

    def print_tree(self, level=0):
        print(" " * level * 2 + str(self.data))  # Print the node with indentation
        for child in self.children:
            child.print_tree(level + 1)  # Recursively print child nodes


# Example usage
root = TreeNode("CEO")
head_of_sales = TreeNode("Head of Sales")
head_of_marketing = TreeNode("Head of Marketing")
sales_executive = TreeNode("Sales Executive")
marketing_executive = TreeNode("Marketing Executive")

root.add_child(head_of_sales)
root.add_child(head_of_marketing)
head_of_sales.add_child(sales_executive)
head_of_marketing.add_child(marketing_executive)

root.print_tree()
