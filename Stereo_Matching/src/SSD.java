public class SSD implements MatchingCost {
  public double matchingCost(double[][] left, double[][] right) {
    double cost = 0;

    int M = left.length, N = left[0].length;
    for (int i = 0; i < M; i++)
      for (int j = 0; j < N; j++) {
        cost += Math.pow(left[i][j] - right[i][j], 2);
      }

    return cost;
  }

  // It should not be used.
  public double matchingCostLab(int[][] left, int[][] right, int[][] leftLab, int[][] rightLab) {return 0;}
}
