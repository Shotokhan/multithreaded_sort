# multithreaded_sort
Performance evaluation of multithreaded merge sort against standard one. <br>
Test parameters can be found and modified in config.JSON <br>
Data is exported to CSV. <br>
The parallel algorithm is adaptive with respect to the number of available cores, i.e. if there are 4 cores, there will a maximum of 4 threads running simultaneously. Furthermore, if there are 6 cores, still 4 threads will be in the running state at the same time: for simplicity's sake, since merge sort recursion is a full binary tree, the maximum number of threads is rounded down to the highest power of 2 lower than or equal to the number of available cores. <br>
