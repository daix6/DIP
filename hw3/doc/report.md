# DIP Homework 3: 
## 戴旋, 13331043

## 1 练习

### 1.1 旋转

傅里叶变换的共轭满足$F(u,v) = F^{\*}(-u,-v)$。故有以下式子成立：

$$\begin{align\*}
  \mathfrak{F}^{-1}\[F^{\*}(u,v)\] & = \sum_{u=0}^{M-1}\sum_{v=0}^{N-1}F(-u, -v)e^{j2\pi(-ux/M-vy/N)}\\\\
  & = \sum_{u=0}^{M-1}\sum_{v=0}^{N-1}F(-u, -v)e^{j2\pi(u(-x)/M+v(-y)/N)} \\\\
  & = f(-x, -y)
\end{align\*}$$

f(x,y)经过傅里叶变换变成了f(-x,-y)，即相当于绕中心旋转了180°，产生了Fig.1(b)的效果。

### 1.2 傅里叶频谱

原图中，边缘相对偏白，像素值偏大。在给周围填充了像素值为0的一系列点之后，其原来的边缘处会产生差距很大的转变，而不是平滑过渡。这些巨大的转变体现在频率域中的水平方向与垂直方向的高频部分。因此频谱图中沿着水平轴与竖直轴的的信号长度有了很大的提升。

### 1.3 低通与高通

1. 如下。

$$\begin{align\*}
  f(x)\ast g(x) & = f(x-1,y-1) + 2f(x,y-1) + f(x+1,y-1) - f(x-1,y+1) - 2f(x,y+1) - f(x+1,y+1)
\end{align\*}$$
傅里叶变换：
$$\begin{align\*}
  G(u,v) & = \mathfrak{F}\[g(x,y)\] \\\\
  & = (e^{j2\pi(-u/M-v/N)} + 2e^{-j2\pi v/N} + e^{j2\pi(u/M-v/N)} \\\\ 
  & - e^{j2\pi(-u/M+v/N)} - 2e^{j2\pi v/N} - e^{j2\pi(u/M+v/N)})F(u,v) \\\\
  & = H(u,v)F(u,v) \\\\
  H(u,v) & = e^{j2\pi(-u/M-v/N)} + 2e^{-j2\pi v/N} + e^{j2\pi(u/M-v/N)} \\\\ 
  & - e^{j2\pi(-u/M+v/N)} - 2e^{j2\pi v/N} - e^{j2\pi(u/M+v/N)} \\\\
  & = -2jsin\[2\pi(u/M+v/N)\] - 4jsin(2\pi v/N) - 2jsin\[2\pi(-u/M+v/N)\] \\\\
  & = -4j(sin2\pi(v/N)(1 + cos2\pi (u/M)))
\end{align\*}$$

所以频率域对应的滤波器H(u,v)为：
$$-2j\lbrace sin\[2\pi(u/M+v/N)\] + 2sin(2\pi v/N) + sin\[2\pi(-u/M+v/N)\]\rbrace$$

2. 高通滤波器

### 可交换性

## 2 编程
