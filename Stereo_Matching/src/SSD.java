public class SSD implements MatchingCost {
  public double matchingCost(int[][] left, int[][] right) {
    double cost = 0;

    int M = left.length, N = left[0].length;
    for (int i = 0; i < M; i++)
      for (int j = 0; j < N; j++)
        cost += Math.pow(Math.abs(left[i][j] - right[i][j]), 2);

    return cost;
  }

  // It should not be used.
  public double matchingCost(int[][] left, int[][] right, int[][] leftLab, int[][] rightLab) {return 0;}
}
