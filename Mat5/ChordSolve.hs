module ChordSolve where
-- chordSolver - рассчитывает список приближений корня функции
-- Параметры:
-- f - (Double->Double) - функция для поиска корня
-- xs - [Double] - список приближений
-- Локальные определения:
-- x - Double - новое вычисленное приближение
chordSolver::(Double->Double)->[Double]->[Double]
chordSolver f xs=xs++zipWith (x) (chordSolver f xs) (tail (chordSolver f xs))
                where
                    x xn xn1=xn-(xn-xn1)*f(xn)/(f(xn)-f(xn1))
-- firstWhenEpsOrCount - возвращает первый элемент списка, для которого 
-- выполнено условие точности либо некоторое количество итераций.
-- Параметры:
-- xs - [Double] - список приближений
-- (eps,n) - (Double,Double) - значение точности и лимит итераций
firstWhenEpsOrCount::(Double,Double)->[Double]->Double                    
firstWhenEpsOrCount (eps,n) (x:xs)|(abs(x-head xs)>eps) && (n>0) = 
                                        firstWhenEpsOrCount (eps,(n-1)) (xs) 
                                  |otherwise = head xs

-- chordSolve - расчет корня функции до выполнения условия точности 
-- либо до превышения лимита итераций.
-- Параметры:
-- f - (Double->Double) - функция для поиска корня
-- (x0,x1) - (Double->Double) - начальные приближения
-- (eps,maxCount) - (Double,Double) - значение точности и лимит итераций
chordSolve::(Double->Double)->(Double,Double)->(Double,Double)->Double
chordSolve f (x0,x1) (eps,maxCount)=firstWhenEpsOrCount  (eps,maxCount) 
                                            (chordSolver f [x0,x1]) 

f::Double->Double
f x=log(log x) - exp(-x^2)

