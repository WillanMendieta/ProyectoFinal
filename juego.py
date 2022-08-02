import cv2
import numpy as np 
import imageio
import pyautogui

posicionXbola=400                         
posicionYdeJugador=650                                             
vid_writer = imageio.get_writer('VideoJuego.avi')
kernel = np.ones((6,6),np.uint8)# Kernel usando para la tanformacion morfologica
while True:
    #posicionXMouse=550         
    pyautogui.typewrite(["space"])     
    #Marco I= 200 H 220 D 650 L 750
    capPantalla = pyautogui.screenshot(region=(220, 220, 630, 750))#Captura la pantalla
    capPantalla = np.array(capPantalla)#convierte la Pantalla en array para por ser trabajar
    capPantalla = cv2.cvtColor(capPantalla, cv2.COLOR_RGB2BGR) # se comvierte a BGR
    apertura = cv2.morphologyEx(capPantalla, cv2.MORPH_OPEN, kernel)#Limpieza de ruido mediante dilatacion
    imag_Bordes = cv2.Canny(apertura,630, 750,apertureSize = 5)# se obtiene los bordes 
    contours, hierarchy  = cv2.findContours(imag_Bordes,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#detectamos los contornos de la imagen
    #Se recorre los n contornos encontrados de la imagen 
    for c in contours:
        ((x, y), radius) = cv2.minEnclosingCircle(c) #  permite encontrar el círculo que cubre completamente el objeto con un área mínima.
        if radius>8:
            #control de acciones  deter     minando la cantidad de pixeles a tomarce encuenta.
            if y>100  and y<750:
                cv2.circle(capPantalla, (int(x), int(y)), 70,(255, 0, 255), 1) 
                #cv2.circle(capPantalla, (int(posicionXMouse), int(500)), 70,(255, 255, 0), 25)
                posicionXbola=x   
    #cv2.circle(capPantalla, (int(posicionXbola), int(200)), 70,(255, 255, 0), 20)#se dibuja el circulo posicion de la bola
    pyautogui.moveTo(int(posicionXbola+250),posicionYdeJugador)#ubica el cursor 
    #cv2.circle(capPantalla, (int(300), int(posicionYdeJugador)), 70,(255, 255, 0), 4)#se dibuja el circulo posicion del jugador
    
    Pantalla1 = cv2.cvtColor(capPantalla, cv2.COLOR_BGR2GRAY)# se covierte de nuevo para poder concatenar las dos pantallas tanto la del juego
    # como la deteccion de bordes
    unido = cv2.hconcat([Pantalla1 ,imag_Bordes])#concatena las pantallas
    video = cv2.resize(unido,(700,600))# se realiza un resize para tener dimenciones cuerentes al mostrar el video.

    cv2.imshow( "Video",  video )    #muestra el video             
    
    vid_writer.append_data(video) # graba el video 
    
    if (cv2.waitKey(23) == 27):#condicion de salida 
        break   

vid_writer.close()#cierra la grabacion del video 

cv2.destroyAllWindows() #cierra todas las ventanas.