module Main where
--rectIntegral::(Double->Double)->(Double,Double)->Double->Double
rectIntegral f (a,b) n=sum (map f [a+h/2,a+3*h/2..b-h/2])*h
                        where
                            h=(b-a)/n
--lastWhenEps::[Double]->Double->Double                            
lastWhenEps (x0:x1:xs) eps |abs(x0-x1)>eps = lastWhenEps (x1:xs) eps
                           |otherwise = x1
--rectIntegrate::(Double->Double)->(Double,Double)->Double->Double                           
rectIntegrate f (a,b) eps = lastWhenEps (map (rectIntegral f (a,b)) [n0,n0*2..]) eps
                             where 
                                n0=8
main::IO ()
main = do
    putStr $ "Введите a: "
    raw_a<-getLine
    putStr $ "Введите b: "
    raw_b<-getLine
    putStr $ "Введите eps: "
    raw_eps<-getLine
    let 
        a=read raw_a;b=read raw_b;eps=read raw_eps
        res=rectIntegrate (\x->sin x) (a,b) eps
    putStrLn $ "Результат: "
    print res