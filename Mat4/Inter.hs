module Main where
import Prelude hiding (catch)
import Control.Exception
import Graphics.UI.Gtk
import Graphics.UI.Gtk.Builder
import MyIntegral 


getValue:: Entry->IO (Double)
getValue entry=do
    y<-get entry entryText
    evaluate (read y)
 
onClickExit=mainQuit

getValues::[Entry]->IO [Double]
getValues xs=getValues' xs []

getValues'::[Entry]->String->IO [Double]
getValues' [] ers |ers==[]= return []
                  |otherwise= error ers
                    
getValues' (x:xs) ers=do
    y<-try(getValue x)::IO(Either SomeException Double)
    
    case y of
        Left e->do
            v<-entryGetText x
            vs<-getValues' xs (ers++"Неправильное значение: \"" ++ v++"\"!\n")
            return vs
        Right v->do
            vs<-getValues' xs ers
            return (v:vs)
main::IO ()
main = do
   let
        
   initGUI
   gtkbuilder<-builderNew
   builderAddFromFile gtkbuilder "gui.glade"
   let
        showFail::SomeException-> IO()
        showFail e=do
            dlg<-messageDialogNew Nothing [DialogModal] MessageError 
                ButtonsClose ("Ошибки:\n"++ show e) 
            _<-dialogRun dlg
            widgetDestroy dlg
        onClickRun=do
            entryA <- builderGetObject gtkbuilder castToEntry "entry1"
            entryB <- builderGetObject gtkbuilder castToEntry "entry2"
            entryEps <- builderGetObject gtkbuilder castToEntry "entry3"
            labelResult <- builderGetObject gtkbuilder castToLabel "labelResult"
            [a,b,eps]<-getValues [entryA,entryB,entryEps]
            if a==b then error "Границы равны!" else do             
                if eps<=0 then error "Точность меньше/равна 0!" else do
                    let
                        res=rectIntegrate f (a, b) (eps) 
                    set labelResult [labelText:="Результат: "++ show res] 
   window    <- builderGetObject gtkbuilder castToWindow "window1"
   buttonRun <- builderGetObject gtkbuilder castToButton "buttonRun"
   onClicked buttonRun (catch onClickRun showFail)
   buttonExit <- builderGetObject gtkbuilder castToButton "button2"
   onClicked buttonExit onClickExit
   onDestroy window mainQuit
   widgetShowAll window
   mainGUI

