module MyIntegral where

-- rectIntegral - расчет определенного интеграла методом средних прямоугольников
-- при указанном количестве шагов.
-- Возвращает рассчитанной значение определенного интеграла.
-- Параметры:
-- f - (Double->Double) - интегрируемая функция
-- (a,b) - (Double,Double) - границы интегрирования
-- n - Double - число шагов изменения аргумента функции
-- Локальные определения:
-- h - Double - шаг изменения аргумента функции
rectIntegral::(Double->Double)->(Double,Double)->Double->Double
rectIntegral f (a,b) n=sum (map f [a+h/2,a+3*h/2..b-h/2])*h
                        where
                            h=(b-a)/n

-- firstWhenEps - возвращает первый элемент списка, для которого 
-- выполнено условие точности.
-- Параметры:
-- xs - [Double] - список приближений
-- eps - Double - значение точности
firstWhenEps::[Double]->Double->Double                            
firstWhenEps (x:xs) eps |abs(x-head xs)>eps = lastWhenEps (xs) eps
                       |otherwise = head xs

-- rectIntegrate - расчет определенного интеграла методом средних прямоугольников
-- до достижения указанной точности.
-- Параметры:
-- f - (Double->Double) - интегрируемая функция
-- (a,b) - (Double,Double) - границы интегрирования
-- eps - Double - значение точности
-- Локальные определения:
-- n0 - Double - первоначальное количество шагов
rectIntegrate::(Double->Double)->(Double,Double)->Double->Double                           
rectIntegrate f (a,b) eps = lastWhenEps (map (rectIntegral f (a,b)) 
                                (map (\x->2^x) [n0,n0+1..])) eps
                             where 
                                n0=4
f x=x/(1+x^2)

