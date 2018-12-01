mod maxminheap;
extern crate rand;

use rand::prelude::*;
use maxminheap::MaxMinHeap;

fn main() {
    let mut heap = MaxMinHeap::new(vec![100, 10, 20, 50, 60, 70, 80, 30, 40, 50]);

    for _ in 1..10000 {
        heap.insert(rand::thread_rng().gen_range(0, 5000));
    }

    heap.replace_maximum(0, 0);
    
    if !heap.is_valid(0) {
        panic!("Invalid heap");
    }

    println!("Heap max: {}, Heap min: {}", heap.max(), heap.min());
}