//code implements a binary search tree

#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>

#ifndef BINTREE_H
#define BINTREE_H

// Node class given by staff
typedef struct node {
	int node_id;
	int data;
	struct node* left_child;
	struct node* right_child;

} node;

///*** DO NOT CHANGE ANY FUNCTION DEFINITIONS ***///
// Declare the tree modification functions below...
void look_left();
void look_right();
int find_left();
int find_right();
void free_left();
void free_right();
void free_node();
void insert_node();
int find_node_data();

#endif


node *root = NULL;

//helper function for insert_node()
void look_left(node* parent, int node_id, int data) {
	//if no left child, insert node into left child of parent
	if (parent->left_child == NULL) {
		parent->left_child = (node*)malloc(sizeof(node));
		parent->left_child ->node_id = node_id;
		parent->left_child ->data = data;
		parent->left_child ->left_child = NULL;
		parent->left_child ->right_child = NULL;
	}
	//else recurse on left child if node_id < left child's id, recurse on right child if node_id is larger
	else {
		if (node_id < parent->left_child ->node_id) {
			look_left(parent->left_child, node_id, data);
		}
		else if (node_id > parent->left_child ->node_id) {
			look_right(parent->left_child, node_id, data);
		}
	}
}

//helper function to insert node
void look_right(node* parent, int node_id, int data) {
	//if no right child, insert into right child
	if (parent->right_child == NULL) {
		parent->right_child = (node*)malloc(sizeof(node));
                parent->right_child ->node_id = node_id;
                parent->right_child ->data = data;
                parent->right_child ->left_child = NULL;
                parent->right_child ->right_child = NULL;
        }
	//else recurse to left if node id < right child's id, recurse to right if node id > right child's id
    else {
        if (node_id < parent->right_child->node_id) {
                look_left(parent->right_child, node_id, data);
            }
        else if (node_id > parent->right_child ->node_id) {
                look_right(parent->right_child, node_id, data);
            }
        }
}

//helper function to find node data
int find_left(node* parent, int  node_id) {
	//if no left child, return error
	if (parent->left_child == NULL) {
		printf("Error. Node not in tree. Cannot find data.\n");
		return 0;
	}
	else {
		//if search id = current node id, pring data
		if (node_id == parent->left_child->node_id) {
			printf("%d\n", parent->left_child->data);
			return 0;
		}
		//else recurse to left or right based on node id
		else if (node_id < parent->left_child->node_id) {
			find_left(parent->left_child, node_id);
		}
		else {
			find_right(parent->right_child, node_id);
		}
	}
}

//helper function to find node data
int find_right(node* parent, int node_id) {
	//if no right child, give error
	if (parent->right_child == NULL) {
		printf("Error. Node not in tree. Cannot find data.\n");
                return 0;
        }
    else {
		//else if search node id = current node id, print data
        if (node_id == parent->right_child->node_id) {
			printf("%d\n", parent->right_child->data);
            return 0;
            }
		//else recurse to left or right based on node id
        else if (node_id < parent->right_child->node_id) {
            find_left(parent->right_child, node_id);
            }
        else {
            find_right(parent->right_child, node_id);
        }
    }
}

//helper function to free node
//searches like find_left/right, except frees space when node is found
void free_left(node* parent, int node_id) {
	if(parent->left_child == NULL) {
		printf("Error. Node not in tree. Cannot free memory.\n");
	}
	else {
		if (node_id == parent->left_child->node_id) {
			free(parent->left_child);
		}
		else if (node_id < parent->left_child->node_id) {
			free_left(parent->left_child, node_id);
		}
		else {
			free_right(parent->left_child, node_id);
		}
	}
}

//helper function to free node
//functions like free_left, but to the right
void free_right(node* parent, int node_id) {
	if(parent->right_child == NULL) {
                printf("Error. Node not in tree. Cannot free memory.\n");
        }
        else {
                if (node_id == parent->right_child->node_id) {
                        free(parent->right_child);
                }
                else if (node_id < parent->right_child->node_id) {
                        free_left(parent->right_child, node_id);
                }
                else {
                        free_right(parent->right_child, node_id);
                }
        }
}

// Insert a new node into the binary tree with node_id and data
void insert_node(int node_id, int data) {
	//if no root, create one
	if (root == NULL){
		root = (node*)malloc(sizeof(node));
		root->node_id = node_id;
		root->data = data;
		root->left_child = NULL;
		root->right_child = NULL;
	}
	//else search the tree
	else {
		if (node_id < root->node_id) {
			look_left(root, node_id, data);
		}
		else {
			look_right(root, node_id, data);
		}
	}
}

// Find the node with node_id, and return its data
int find_node_data(int node_id) {
	//if no root, give error
	if (root == NULL) {
		printf("Error. No nodes in tree. Cannot find data.\n");
		return 0;
	}
	//else search tree using helper functions
	else {
		if (root->node_id == node_id) {
			printf("%d ", root->data);
			return 0;
		}
		else if (node_id < root->node_id) {
			find_left(root, node_id);
		}
		else {
			find_right(root, node_id);
		}
	}
}

//Free all memory allocated to nodes in program.
void free_node(int node_id) {
	//if no root, give error
	if (root == NULL) {
		printf("Error. No nodes in tree. Cannot free memory.\n");
	}
	//else search the tree using helper functions
	else {
		if (root->node_id == node_id) {
			free(root);
		}
		else if (node_id < root->node_id) {
			free_left(root, node_id);
		}
		else {
			free_right(root, node_id);
		}
	}
}


