module Euler where
f' k p x y=k/x^2-p*y^2::Double
euler::(Double->Double->Double)->[Double]->Double->[Double]
-- Функция euler - функция решения дифференциального уравнения 
--    по явному методу Эйлера.
-- Возвращает массив значений указанных узлов для функции-решения уравнения.
-- Параметры:
-- f - (Double->Double->Double) – производная искомой функции
-- x - [Double] - список узлов для поиска значений функции
-- y0 – Double – начальное условие – значение функции в первом узле.
-- Локальные переменные:
-- euler' - [Double] - список значений решения уравнения в заданных узлах
-- derivat - ([Double],[Double]) - кортеж списка значений производной в узлах
    -- и шага между соседними узлами.
-- deltas - [Double] - список шагов между соседними узлами.
-- derivates - [Double] - список значений производной в узлах.
euler f' xs y0=euler' where
    euler'=y0:zipWith getNewValue euler' derivat
        where
            getNewValue y (y',h)=y+y'*h
            derivat = zip (derivatives xs) (deltas xs)
            deltas []=[]
            deltas (x:[])=[]
            deltas (x0:x1:xs)=x1-x0:deltas(x1:xs)
            derivatives xs=zipWith f' xs euler'
            
