#! /usr/bin/env python3
from sys import stdin,stdout
from math import sqrt
# Хелло
def solvesys(a,e,iter_check=True):
    '''
    Функция solvesys - функция решения СЛАУ.
    Возвращает - решение и статистику о решении.
    Если решение не найдено, возвращает None и
    поясняющее сообщение.
        
        solvesys(a,e,iter_check=True)

    Параметры:
    a - расширенная матрица СЛАУ
    e - точность вычислений
    iter_check - флаг необходимости проверки сходимости
        на каждом шаге итераций
    Локальные переменные:
    at - матрица системы, приведенная к трапец. виду
        (с полным переупорядовачением)
    r,rext - ранги основной и расширенной матриц СЛАУ
    '''
    at=a
    r,rext=rank(at)
    if r<len(a[0])-1:
        if r<rext:
            return (None,"Система не имеет решений!")
        else:
            return (None,"У системы бесконечно много решений!")
    else:
        if not is_positive(a):
            a=at_matr(a)
            
        return zeidel(a,e,iter_check)

def gauss_transform(a):
    '''
    Функция gauss_transform - функция
    преобразования расширенной матрицы СЛАУ
    с полным переупорядовачиванием.
    Возвращает преобразованную матрицу.

        gauss_transform(a)
        
    Параметры:
    a - расширенная матрица СЛАУ
    Локальные переменные:
    at - копия матрицы а для преобразования.
    i,j,k - переменные-счетчики для перебора элементов матрицы a.
    i2,j2 - координаты элемента для перестановки на диагональ
        матрицы
    factor - коэффициент домножения на слагаемую строку матрицы
    '''
    at=[[j for j in i] for i in a]
    def index_of_max():
        '''
        index_of_max - функция индексов нахождения максимального по модулю элемента 
        в подматрице (i,i,n,n) в основной матрице СЛАУ A(n x n).
        Внутренняя функция функции gauss_transform.
            
            index_of_max()
        
        Переменные объемлющей функции:
        at - копия матрицы а для преобразования.
        i - переменная-счетчик; кордината левого верхнего угла подматрицы
        Локальные переменные:
        m - модуль максимального элемента
        j,k - переменные-счетчики для перебора элементов матрицы at.
        i2,j2 - индексы максимального элемента
        '''
        nonlocal at,i
        m=abs(at[i][i]);i2=i;j2=i;
        for j in range(i,len(at)):
            for k in range(i,len(at)):
                if abs(at[j][k])>m:
                    m=abs(at[j][k]);i2=j;j2=k
        return (i2,j2)

    for i in range(0,len(at)):
        i2,j2=index_of_max()
        
        if at[i2][j2]==0:
            return at
        if i2!=i:
            for j in range(i,len(at[i])):
                at[i][j],at[i2][j]=at[i2][j],at[i][j]
        if j2!=i:    
            for j in range(0,len(at)):
                at[j][i],at[j][j2]=at[j][j2],at[j][i]
        for j in range(i+1,len(at)):
            factor=at[j][i]/at[i][i];at[j][i]=0
            for k in range(i+1,len(at[i])):
                at[j][k]-=at[i][k]*factor;
                if abs(at[j][k])<1e-10:
                    at[j][k]=0
    
    return at

def is_positive(a):
    '''
    Функция is_positive - функция проверки матрицы на диагональное преобладание.
    Если матрица имееет диагональное преобладание, возвращает True,
    иначе возвращает False.
        is_positive(a)
    Параметры:
    a - расширенная матрица СЛАУ
    Локальные переменные:
    k - количество преобладающих диагональных элементов
    s - сумма модулей элементов строки без диегонального.
    i,j - переменные-счетчики для перебора элементов матрицы a.
    '''
    k=0
    for i in range(0,len(a)):
        s=0
        for j in range(0,len(a)):
            if i!=j:
               s+=abs(a[i][j])
        if a[i][i]>s:
            k+=1
        elif a[i][i]<s:
            return False

    if k>0:
        return True
    else:
        return False                   

def rank(a):
    '''
    rank - функция расчета рангов основной и расширенной матриц СЛАУ.
        
        rank(a)
    
    Параметры:
    a - расширенная матрица СЛАУ
    Локальные переменные:
    at - преобразованная в трапециедальную матрица а
    r,rext - r,rext - ранги основной и расширенной матриц СЛАУ 
    i - переменная-счетчик для перебора элементов матрицы a.
    '''
    at=gauss_transform(a)
    r=0;rext=0;
    for i in range(0,len(a)):
        if at[i][i]!=0:
            r+=1
    row_end=len(a[i])-1
    for i in range(0,len(a)):
        if at[i][row_end]!=0:
            rext+=1
    return (r,rext)
            
def at_matr(a):
    '''
    at_matr - функция домножения расширенной матрицы СЛАУ на транспонированную основную.
    
        at_matr(a)
        
    Параметры:
    a - расширенная матрица СЛАУ
    Локальные переменные:
    an - преобразованная матрица СЛАУ
    i,j,k - переменные-счетчики для перебора элементов матрицы a.
    '''
    an=[]
    for i in range(0,len(a)):
        an.append([])
        for j in range(0,len(a[0])):
            an[i].append(0)
            for k in range(0,len(a)):
                
                an[i][j]+=(a[k][i]*a[k][j] )# an[i,j]:=an[
    return an

def norm(a):
    '''
    norm - функция расчета нормы матрицы alpha для методов
    простых итераций и Гаусса-Зейделя.
        
        norm(a)
    
    Параметры:
    a - расширенная матрица СЛАУ
    Локальные переменные:
    s - сумма квадратов строки матрицы alpha
    line - строка матрицы alpha
    a_ij - текущий элемент alpha 
    i,j - переменные-счетчики.
    '''
    s=0;i=0
    for line in a:
        j=0
        for a_ij in line:
            if i!=j:
                s+=a_ij*a_ij
            j+=1
        s/=a[i][i]*a[i][i]
        i+=1
    return sqrt(s)

def zeidel(a,e,iter_check):
    '''
    zeidel - функция решения СЛАУ по методу Гаусса-Зейделя
    Возвращает - решение и статистику о решении.
    Если решение не найдено, возвращает None и
    поясняющее сообщение.
    
        zeidel(a,e,iter_check)
        
    Параметры:
    a - расширенная матрица СЛАУ
    e - точность вычислений
    iter_check - флаг необходимости проверки сходимости
        на каждом шаге итераций
    Локальные переменные:
    x - решение СЛАУ
    stats - статистика решения
    n - коэффициент оценки погрешности
    ek0,ek - точность на предыдущем и текущем шаге
    '''
    stats={'сложений':0,
           'вычитаний':0,
           'умножений':0,
           'делений':0,
           'итераций':0}
    def z_step():
        '''
        z_step - функция итерации метода Гаусса-Зейделя.
        Возвращает рассчитанное решение и точность этого решения.
        
            z_step()
            
        Переменные объемлющей функции:
        a - расширенная матрица СЛАУ
        x - решение СЛАУ
        stats - статистика решения
        Локальные переменные:
        ek - точность на текущем шаге
        i,j - переменные-счетчики для перебора элементов матрицы a.
        '''
        nonlocal a,x,stats
        ek=0;
        for i in range(0,len(a)):
            p=x[i];x[i]=0;
            for j in range(0,len(a)):
                if i!=j:
                    x[i]+=a[i][j]*x[j]
                    stats['умножений']+=1;stats['сложений']+=1
            x[i]=(a[i][len(a[i])-1]-x[i])/a[i][i]
            stats['делений']+=1;stats['вычитаний']+=1
            ek+=abs(x[i]-p)
            
            stats['итераций']+=1
        return  x,ek
    if norm(a)!=1:
        n=abs(norm(a)/(1-norm(a)))
    else:
        n=1
    x=[0 for i in range(0,len(a))]
    x,ek=z_step();ek0=ek+1
    while (not iter_check or (ek0>ek))and(n*ek>=e):
        ek0=ek;
        x,ek=z_step()
    if ek>ek0:
        return (None,
            'Сходимость нарушается на шаге {}!'.format(stats['итераций']))        
    return x,stats

def read_matr(file):
    '''
    read_matr - функция чтения матрицы из файла
    '''
    a=[];i=0
    for line in file:
        a.append([]);
        for chunk in line.split(' '):
            a[i].append(float(chunk))
        if i>0 and len(a[i])!=len(a[i-1]):
            return None
        i+=1
    return a

def new_matrix():
    '''
    new_matrix - функция заполнения расширенной матрицы СЛАУ
    '''
    variant=input('\n'.join(("Заполните матрицу системы.",
                  "1 - ввести из файла,",
                  '2 - ввести с клавиатуры,',
                  'иначе - выход.',
                  'ответ: ')))
    if variant=='1':
        try:
            with open(input('Введите имя файла: ')) as f:
                return read_matr(f)
        except IOError as err:
            print('Ошибка открытия файла: ',err)
    elif variant=='2':
        print('\n'.join(('Введите расширенную матрицу системы:',
                         '(окончание ввода - COTROL+D)')))
        return read_matr(stdin)
    else:
        quit()

def write_file(f,opts,solve):
    '''
    write_file - функция записи решения и статистики решения СЛАУ в файл.
    '''
    print('Расширенная матрица системы:',file=f)
    for l in opts[0]:
        for n in l:
            print(n,end=' ',file=f)
        print('',file=f)
    print('Точность решения: ',opts[1],file=f)
    print('Решение: ',file=f)
    i=0;
    for x in solve[0]:
        i+=1
        print('x[{}]={}'.format(i,x),file=f)
    print('Статистика:',file=f)
    for k,v in solve[1].items():
        print('Число {}: {}'.format(k,v),file=f)

def write_data(opts,solve):
    '''
    write_data - функция вывода решения и статистики решения СЛАУ в файл
    '''
    variant=input('\n'.join(("Выведите результаты работы.",
                  "1 - вывести в файл,",
                  '2 - вывести на экран,',
                  'иначе - выход.',
                  'ответ: ')))
    if variant=='1':
        try:
            with open(input('Введите имя файла: '),'a') as f:
                write_file(f,opts,solve)
        except IOError as err:
            print('Ошибка открытия файла: ',err)
    elif variant=='2':
        write_file(stdout,opts,solve)
    else:
        quit()

def get_data():
    '''
    get_data - функция ввода расширенной матрицы СЛАУ и параметров расчета
    '''
    try:
        a=new_matrix();
        if not a:
            raise ValueError()
    except ValueError:
        print('Ошибка при вводе матрицы!');
        quit();
    try:
        e=float(input('Введите точность вычислений: '));
    except ValueError:
        print('Введено не число!');
        quit();
    chk=input('Проверять сходимость на каждом шаге?([yes]/no): ').upper()!='NO'
    return a,e,chk
if __name__=='__main__':
    opts=get_data()
    solve=solvesys(*(opts))
    if solve[0]:
        write_data(opts,solve)
    else:
        print(solve[1])
    input()

