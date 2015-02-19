def get_diff(x,i,k,f,l):
    '''
    get_diff - рекурсивная функция расчета разделенных разностей.
      Значение функции – некоторая разделенная разность.
      Возвращает через параметр список разделенных разностей.
    Параметры:
    x - список аргументов функции,
    i - индекс разделенной разности
    k - степень разделенной разности
    f - список значений функции от аргументов х
    l - список разделенных разностей
    '''
    if k==0:
        if i==0:
            l[0]=f[0]
            return l[0]
        return f[i]
    else:
        if i==0:
            l[k]=(get_diff(x,i+1,k-1,f,l)-
                  get_diff(x,i,k-1,f,l))/(x[i+k]-x[i])
            return l[k]
        return (get_diff(x,i+1,k-1,f,l)-
                get_diff(x,i,k-1,f,l))/(x[i+k]-x[i])
    
def mult_poly(l1,l2):
    '''
    mult_poly - функция умножения многочленов.
      Возвращает многочлен-произведение.
    Параметры:
    l1,l2 - список коэффициентов полиномов-множителей
    Локальные переменные:
    res - список коэффициентов полинома-произведения
    i,j - переменные счетчики для доступа к элементам списков
    '''
    res=[0 for i in range(0,len(l1)+len(l2)-1)]
    for i in range(0,len(l1)):
        for j in range(0,len(l2)):
            res[i+j]+=l1[i]*l2[j]
    return res

def add_poly(l1,l2):
    '''
    add_poly - функция суммирования многочленов.
      Возвращает многочлен-сумму.
    Параметры:
    l1,l2 - список коэффициентов полиномов-слагаемых
    Локальные переменные:
    res - список коэффициентов полинома-суммы
    i,j - переменные счетчики для доступа к элементам списков
    m - максимальная из степеней многочленов-сумм
    '''
    res=[]
    m=min(len(l1),len(l2))
    for i in range(0,m):
        res.append(l1[i]+l2[i])
    if len(l1)>len(l2):
        for i in range(m,len(l1)):
            res.append(l1[i])
    else:
        for i in range(m,len(l2)):
            res.append(l2[i])
        
    return res

def cmult_poly(c,l):
    '''
    cmult_poly - функция умножения многочлена на число.
      Возвращает многочлен-произведение.
    Параметры:
    c - константа-множитель,
    l - список коэффициентов полинома-множителя
    Локальные переменные:
    res - список коэффициентов полинома-произведения
    i - переменная счетчик для доступа к элементам списка
    '''
    res=[]
    for i in l:
        res.append(c*i)
    return res

def make_newton_poly(x,f):
    '''
    make_newton_poly - функция расчета коэффициентов
    интерполяционного многочлена
      Ньютона с разделёнными разностями для таблично заданной функции.
      Возвращает коэффициенты многочлена.
    Параметры:
    x - список аргументов функции,
    f - список значений функции от аргументов х
    Локальные переменные:
    d - список разделенных разностей
    res - коэффициенты многочлена Ньютона
    l - коэффициенты многочлена вида (x-x0)(x-x1)...
    '''
    d=[0 for i in x]
    get_diff(x,0,len(x)-1,f,d)
    res=[d[0]];l=[1]
    for i in range(0,len(x)-1):
        l=mult_poly(l,[-x[i],1])
        res=add_poly(res,cmult_poly(d[i+1],l))
    return res

def input_data():
    x=input_x()
    return x,input_f(x)

def func(x):
    return x**4+3*x-1

def input_x():
    x=[];
    answ=input('Хотите ввести аргументы функции вручную? y,[n]: ');
    if answ=='y':
        n=int(input('Введите количество аргументов: '))
        for i in range (0,n):
            x_i=input('Введите х[{}]: '.format(i))
            x.append(float(x_i))
    else:
        a=float(input('Введите минимальное значение: '))
        b=float(input('Введите максимальное значение: '))
        if b<a:
            raise ValueError
        step=float(input('Введите шаг изменения: '))
        while a+step<=b:
            x.append(a);
            a+=step
        x.append(b);
    return x

def input_f(x):
    f=[]
    answ=input('Хотите ввести значения функции вручную? y,[n]: ');
    if answ=='y':
        for i in range(0,len(x)):
            f_i=input('Введите f(х[{}]): '.format(i))
            f.append(float(f_i))
    else:
        for i in x:
            f.append(func(i))
    return f

def print_poly(poly):
    if len(poly)>2:    
        for i in range(len(poly)-1,1,-1):
            if poly[i]>0:
                print('+{}x^{}'.format(poly[i],i),end='')
            elif poly[i]<0:
                print('{}x^{}'.format(poly[i],i),end='')
    if len(poly)>1:
        if poly[1]>0:
            print('+{}x'.format(poly[1]),end='')
        elif poly[1]<0:
            print('{}x'.format(poly[1]),end='')
    if poly[0]>0:
        print('+{}'.format(poly[0]),end='')
    elif poly[0]<0:
        print('{}'.format(poly[0]),end='')
    print()
    
if __name__=='__main__':
    try:
        print('Программа строит интерполяционный многочлен Ньютона'
              ' с конечными разностями.')
        x,f=input_data()
    except ValueError as e:
        print("Ошибка ввода данных!\nИнформация об ошибке:",e)
    else:
        poly=make_newton_poly(x,f)
        print_poly(poly)
        print('Программа завершена...');
