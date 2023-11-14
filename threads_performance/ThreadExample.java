public class ThreadExample {
    static int TOTAL_THREADS;
    static int MAX_ITERATIONS;

    public static void main(String[] args) {
        long start = System.currentTimeMillis();
        TOTAL_THREADS = Integer.parseInt(args[0]);
        MAX_ITERATIONS = Integer.parseInt(args[1]);
        Thread[] threads = new Thread[TOTAL_THREADS];
        

        for (int i = 0; i < TOTAL_THREADS; i++) {
            final int tid = i;
            threads[i] = new Thread(() -> count(tid));
            threads[i].start();
        }

        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        long end = System.currentTimeMillis();
        System.out.println((end - start) + "ms");
    }

    static void count(int tid) {
        int counter = 0;
        for (int i = 0; i < MAX_ITERATIONS; i++) {
            counter++;
        }

        // System.out.println("Thread " + tid + " done. Counter= " + counter);
    }
}
