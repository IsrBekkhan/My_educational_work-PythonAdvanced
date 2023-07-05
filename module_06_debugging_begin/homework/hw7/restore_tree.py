from binary_tree_walk import BinaryTreeNode
from re import findall


node_dict = dict()


def get_binary(parent_value: int) -> BinaryTreeNode:
    """
    Рекурсивная-функция, принимающая значение родителя объекта BinaryTreeNode и
    возвращающая его корень

    """
    binary_object: BinaryTreeNode = node_dict.get(parent_value)

    if binary_object:

        if binary_object.left:
            binary_object.left = get_binary(binary_object.left.val)

        if binary_object.right:
            binary_object.right = get_binary(binary_object.right.val)

    return binary_object


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    """
    Функция, подгатавливающая словарь с объектами BinaryTreeNode и вызывающая
    функцию get_binary для получения объекта BinaryTreeNode

    """
    main_parent_value = False

    with open(path_to_log_file, 'r') as log_file:

        for log in log_file.readlines():

            if log.startswith('DEBUG'):

                if not main_parent_value:
                    node_parent, node_left = map(int, findall(r'<BinaryTreeNode\[(\d+)]>', log))
                    main_parent_value = node_parent

                if 'left' in log:
                    node_parent, node_left = map(int, findall(r'<BinaryTreeNode\[(\d+)]>', log))

                    if not node_dict.get(node_parent):
                        node_dict[node_parent] = BinaryTreeNode(node_parent)

                    node_dict[node_parent].left = BinaryTreeNode(node_left)

                if 'right' in log:
                    node_parent, node_right = map(int, findall(r'<BinaryTreeNode\[(\d+)]>', log))

                    if not node_dict.get(node_parent):
                        node_dict[node_parent] = BinaryTreeNode(node_parent)

                    node_dict[node_parent].right = BinaryTreeNode(node_right)

    return get_binary(main_parent_value)


if __name__ == '__main__':
    result_binary_object = restore_tree('walk_log_2.txt')
    print(result_binary_object)

