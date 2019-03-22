use std::cmp;

macro_rules! left {
    ($e:expr) => (2 * $e + 1)
}

macro_rules! right {
    ($e:expr) => (2 * $e + 2)
}

macro_rules! parent {
    ($e:expr) => (($e-1)/2)
}

pub struct MaxMinHeap {
    pub data: Vec<i32>
}

impl MaxMinHeap {
    pub fn new(data: Vec<i32>) -> MaxMinHeap {
        return MaxMinHeap {
            data: data
        };
    }

    pub fn comp(&self, parent: usize, child: usize) -> bool {
        if parent >= self.data.len() || child >= self.data.len() {
            return true;
        }

        let is_parent_max: bool = ((parent + 1) as f32).log2().floor() % 2.0 == 0.0;

        return (is_parent_max && self.data[parent] >= self.data[child]) ||
            (!is_parent_max && self.data[parent] <= self.data[child]);
    
    }

    pub fn is_valid(&self, i: usize) -> bool {
        if i >= self.data.len() {
            return true;
        }

        if !self.comp(i, left!(i)) ||
            !self.comp(i, left!(left!(i))) ||
            !self.comp(i, right!(left!(i))) ||
            !self.is_valid(left!(i)) {
            return false;
        }

        if !self.comp(i, right!(i)) ||
            !self.comp(i, left!(right!(i))) ||
            !self.comp(i, right!(right!(i))) ||
            !self.is_valid(right!(i)) {
            return false;
        }

        return true;
    }

    pub fn max(&self) -> i32 {
        return self.data[0];
    }

    pub fn min(&self) -> i32 {
        return cmp::min(self.data[left!(0)], self.data[right!(0)]);
    }

    pub fn insert(&mut self, key: i32) {
        self.data.push(key);  

        let mut i = self.data.len() - 1;

        if !self.comp(parent!(i), i) {
            self.data.swap(parent!(i), i);
            i = parent!(i);
        }

        while i >= 3 {   // parent!(parent!(i) > 0
            if self.comp(parent!(parent!(i)), i) {
                return;
            }

            self.data.swap(parent!(parent!(i)), i);  
            i = parent!(parent!(i));
        } 
    }

    pub fn replace_maximum(&mut self, i: usize, key: i32) {
        let n = self.data.len();
        // There are no children - OK.
        if left!(i) >= n {
            self.data[i] = key;
            return;
        }

        // Key is larger than the current maximum - OK
        if key >= self.data[i] {
            self.data[i] = key;
            return;
        }

        // Find largest son.
        let mut largest_son = left!(i);        
        if right!(i) < n && self.data[right!(i)] > self.data[largest_son] {
            largest_son = right!(i);
        }

        // Check if the key is smaller than largest son
        if key < self.data[largest_son] {
            let largest_son_value = self.data[largest_son];
            self.data[largest_son] = key;
            
            self.replace_maximum(i, largest_son_value);
            return;
        }

        // Key is now guaranteed to be larger than largest son.

        // If there aren't any grandsons, we're good.
        if left!(left!(i)) >= n {
            self.data[i] = key;
            return;
        }

        // Find largest grandson.
        let mut largest_grandson = left!(left!(i));
        if left!(right!(i)) < n && self.data[left!(right!(i))] > self.data[largest_grandson] {
            largest_grandson = left!(right!(i));
        } 
        if right!(left!(i)) < n && self.data[right!(left!(i))] > self.data[largest_grandson] {
            largest_grandson = right!(left!(i));
        }        
        if right!(right!(i)) < n && self.data[right!(right!(i))] > self.data[largest_grandson] {
            largest_grandson = right!(right!(i));
        }

        self.data[i] = self.data[largest_grandson];
        self.replace_maximum(largest_grandson, key);
    }
}