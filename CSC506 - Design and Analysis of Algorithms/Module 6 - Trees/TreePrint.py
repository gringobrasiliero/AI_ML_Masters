
# Derived from: https://github.com/joowani/binarytree/blob/master/binarytree/__init__.py
# The following license applies to the TreePrint.py file only.
# MIT License

# Copyright_child (c) 2016 Joohwan Oh

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the right_childs
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright_child notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYright_child HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
def _pretty_tree_helper(root_node, curr_index=0):
    if root_node is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    node_repr = str(root_node.data)

    new_root_node_width = gap_size = len(node_repr)
    
    # Get the left_child and right_child sub-boxes, their widths, and root_node repr positions
    l_box, l_box_width, l_root_node_start, l_root_node_end = _pretty_tree_helper(root_node.left_child, 2 * curr_index + 1)
    r_box, r_box_width, r_root_node_start, r_root_node_end = _pretty_tree_helper(root_node.right_child, 2 * curr_index + 2)

    # Draw the branch connecting the current root_node to the left_child sub-box
    # Pad with whitespaces where necessary
    if l_box_width > 0:
        l_root_node = (l_root_node_start + l_root_node_end) // 2 + 1
        line1.append(' ' * (l_root_node + 1))
        line1.append('_' * (l_box_width - l_root_node))
        line2.append(' ' * l_root_node + '/')
        line2.append(' ' * (l_box_width - l_root_node))
        new_root_node_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_node_start = 0

    # Draw the representation of the current root_node
    line1.append(node_repr)
    line2.append(' ' * new_root_node_width)

    # Draw the branch connecting the current root_node to the right_child sub-box
    # Pad with whitespaces where necessary
    if r_box_width > 0:
        r_root_node = (r_root_node_start + r_root_node_end) // 2
        line1.append('_' * r_root_node)
        line1.append(' ' * (r_box_width - r_root_node + 1))
        line2.append(' ' * r_root_node + '\\')
        line2.append(' ' * (r_box_width - r_root_node))
        gap_size += 1
    new_root_node_end = new_root_node_start + new_root_node_width - 1

    # Combine the left_child and right_child sub-boxes with the branches drawn above
    gap = ' ' * gap_size
    new_box = [''.join(line1), ''.join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
        r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root_node positions
    return new_box, len(new_box[0]), new_root_node_start, new_root_node_end
    
def pretty_tree(tree):
    lines = _pretty_tree_helper(tree.root_node, 0)[0]
    return '\n' + '\n'.join((line.rstrip() for line in lines))
