// Условие сходимости
bool converge(double *xk, double *xkp)
{
    for (int i = 0; i < n; i++) 
    {
        if (fabs(xk[i] - xkp[i]) >= eps) 
            return false;
    }
    return true;
}
 
/*
    Ход метода, где:
    a[n][n] - Матрица коэффициентов
    x[n], p[n] - Текущее и предыдущее решения
*/
 
do
{
    for (int i = 0; i < n; i++)
    {
        double var = 0;
        for (int j = 0; j < n; j++)
            if (j != i) var += (a[i][j] * x[j]);
        p[i] = x[i];
        x[i] = (b[i] - var) / a[i][i];
    }
}
while (!converge(x, p));
