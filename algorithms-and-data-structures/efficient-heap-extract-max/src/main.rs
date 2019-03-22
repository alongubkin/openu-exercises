macro_rules! left {
    ($e:expr) => (2 * $e + 1)
}

macro_rules! right {
    ($e:expr) => (2 * $e + 2)
}

macro_rules! parent {
    ($e:expr) => (($e-1)/2)
}

fn heap_shift_up(heap: &mut Vec<i32>, path: &mut Vec<usize>, i: usize) -> usize {
    let n = heap.len();

    // If there are no children - nothing to do.
    if left!(i) >= n {
        return i;
    }

    // Add current node to the path
    path.push(i);
    
    // Check which child is larger
    if right!(i) < n && heap[right!(i)] > heap[left!(i)] {
        heap[i] = heap[right!(i)];
        return heap_shift_up(heap, path, right!(i));
    } else {
        heap[i] = heap[left!(i)];
        return heap_shift_up(heap, path, left!(i));
    }
}

fn find_insert_position(heap: &Vec<i32>, path: &Vec<usize>, left: usize, right: usize, key: i32) -> usize {
    if left >= right {
        return path[left];
    }

    let middle = (left + right) / 2;
    if key < heap[path[middle]] {
        return find_insert_position(heap, path, middle + 1, right, key);
    } else if key > heap[path[middle]] {
        return find_insert_position(heap, path, left, middle, key);
    }

    return path[middle];
}

fn heap_extract_max(heap: &mut Vec<i32>) -> i32 {
    let max = heap[0];

    // STEP 1: Remove the last element of the heap
    let last_element_index = heap.len() - 1;
    let last_element = heap[last_element_index];
    heap.remove(last_element_index);

    // STEP 2: Override the maximum element with its largest son recursively
    let mut path: Vec<usize> = Vec::new();
    let mut invalid_node = heap_shift_up(heap, &mut path, 0);

    if last_element <= heap[parent!(invalid_node)] {
        heap[invalid_node] = last_element;
        return max;
    }

    let path_length = path.len()-1;

    // STEP 3: The invalid node is in an incorrect position. Fix it.
    let insert_position = find_insert_position(&heap, &path, 0, path_length, last_element);
    while invalid_node < insert_position {
        heap[invalid_node] = heap[parent!(invalid_node)];
        invalid_node = parent!(invalid_node);
    }

    heap[insert_position] = last_element;

    return max;
}

fn main() {
    let mut heap: Vec<i32> = vec!(
                        10, 
                5,                  6, 
           1,        2,       4,        3, 
        //  1,  1,    1, 1,    1, 2,      1, 3
    );

    println!("Before: {:?}", heap);
    println!("Max: {}", heap_extract_max(&mut heap));
    println!("After: {:?}", heap);
}
