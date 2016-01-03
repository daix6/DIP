public class NCC implements MatchingCost {
  public double matchingCost(int[][] left, int[][] right) {
    double cost = 0;
    double mean_l = 0, mean_r = 0, std_l = 0, std_r = 0;

    int M = left.length, N = left[0].length;
    for (int i = 0; i < M; i++)
      for (int j = 0; j < N; j++) {
        mean_l += left[i][j];
        mean_r += right[i][j];
      }

    mean_l /= (M * N);
    mean_r /= (M * N);
    
    for (int i = 0; i < M; i++)
      for (int j = 0; j < N; j++) {
        std_l += Math.pow(left[i][j] - mean_l, 2);
        std_r += Math.pow(right[i][j] - mean_r, 2);
      }

    std_l /= (M * N);
    std_r /= (M * N);
    std_l = Math.sqrt(std_l);
    std_r = Math.sqrt(std_r);

    for (int i = 0; i < M; i++)
      for (int j = 0; j < N; j++) {
        cost += (left[i][j] - mean_l) * (right[i][j] - mean_r);
      }

    return 1 - cost / (M * N * std_l * std_r);
  }

  // It should not be used.
  public double matchingCost(int[][] left, int[][] right, int[][] leftLab, int[][] rightLab) {return 0;}
}
