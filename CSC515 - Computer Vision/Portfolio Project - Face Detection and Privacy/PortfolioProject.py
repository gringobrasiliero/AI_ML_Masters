import matplotlib.pyplot as plt
import cv2
import numpy as np
import math

def rotate_face(eye_one, eye_two, img):
    height, width = img.shape[:2]
    if len(eye_one) == 4:
        eye_one_x, eye_one_y, eye_one_w, eye_one_h = eye_one
        eye_two_x, eye_two_y, eye_two_w, eye_two_h = eye_two
        center_x_one = eye_one_x + (eye_one_w//2)
        center_y_one = eye_one_y + (eye_one_h//2)
        center_x_two = eye_two_x + (eye_two_w//2)
        center_y_two = eye_two_y + (eye_two_h//2)
    else:
        center_x_one , center_y_one , eye_one_r = eye_one
        center_x_two , center_y_two, eye_two_r = eye_two
        
    #Radian of the two eye centers
    if center_x_one > center_x_two:
        radian = math.atan2( (center_y_one - center_y_two) , (center_x_one - center_x_two) )
    else:
        radian = math.atan2( (center_y_two - center_y_one) , (center_x_two - center_x_one) )
    #converts Radians to Degrees
    degrees = math.degrees(radian)
   
    rot_mat = cv2.getRotationMatrix2D(center=(width/2, height/2), angle=degrees, scale=1)
    
    display_img = cv2.warpAffine(src=img, M=rot_mat, dsize=(width, height))
    
    #result gets included with final resulting images without markings
    result = cv2.warpAffine(src=img, M=rot_mat, dsize=(width, height))
    return display_img


def get_faces(img, expected_faces, face_cascade):
   
    # convert to grayscale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # detects faces in the input image
    faces = face_cascade.detectMultiScale(gray, 1.25, expected_faces)
    print("# Faces Detected: ",len(faces))
    if len(faces) != expected_faces:
        print("Faces Detected: ",len(faces))
        gaus = cv2.GaussianBlur(gray, (3, 3), 1)
        faces = face_cascade.detectMultiScale(gaus, 1.2 , expected_faces)
        print("# Faces Detected: ",len(faces)) 

        if len(faces) != expected_faces:
            #Sorting by largest area
            faces = sorted(faces, key=lambda face: (face[2] * face[3]), reverse=True)
            faces = faces[0:expected_faces]
        


    for (x,y,w,h) in faces:
       # To draw a rectangle around the detected face  
       ar = float(w)/h
       roi = img[y:y+h, x:x+w]
       view_img(roi, "Face")
       img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    return img, faces


def view_img(img, title):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_degrees(eye_one, eye_two):        
    if len(eye_one) == 4:
        eye_one_x, eye_one_y, eye_one_w, eye_one_h = eye_one
        eye_two_x, eye_two_y, eye_two_w, eye_two_h = eye_two
        center_x_one = eye_one_x + (eye_one_w//2)
        center_y_one = eye_one_y + (eye_one_h//2)
        center_x_two = eye_two_x + (eye_two_w//2)
        center_y_two = eye_two_y + (eye_two_h//2)
    else:
        eye_one_x, eye_one_y, eye_one_r = eye_one
        eye_two_x, eye_two_y, eye_two_r = eye_two
        center_x_one = eye_one_x
        center_y_one = eye_one_y
        center_x_two = eye_two_x
        center_y_two = eye_two_y
                
    if center_x_one > center_x_two:
        radian = math.atan2( (center_y_one - center_y_two) , (center_x_one - center_x_two) )
    else:
        radian = math.atan2( (center_y_two - center_y_one) , (center_x_two - center_x_one) )
    #converts Radians to Degrees
    degrees = math.degrees(radian)
    return degrees

def get_eyes(img, face_coords, image):
    # convert to grayscale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eye_cascade = cv2.CascadeClassifier('C:\opencv\haarcascades\haarcascade_eye.xml')
    # detects faces in the input image
    eyes = eye_cascade.detectMultiScale(gray, 1.5, 2)

    eye_list = []
    print("EYES DETECTED:",len(eyes))

    if len(eyes) < 2:
        gaus = cv2.GaussianBlur(gray, (5, 5), 1)
        
        eyes = eye_cascade.detectMultiScale(gray, 1.2, 2)

    if len(eyes) > 2:
        print("Further Processing needed.")
        print("EYES FOUND",len(eyes))
        i=0
        eye_list = []# list of identified eye pairs, including the area difference and the angle of the two eyes

        while i < len(eyes)-1:
            eye_one = eyes[i]
            eye_two = eyes[i+1]
            area_eye_one = eye_one[2]*eye_one[3]
            area_eye_two = eye_two[2]*eye_two[3]
            area_diff = abs(area_eye_one-area_eye_two)

            degrees = get_degrees(eye_one,eye_two)
            eye_list.append([abs(degrees),area_diff,eye_one, eye_two])
            i+=1
        degrees = get_degrees(eyes[0],eyes[-1])
        area_eye_one = eyes[0][2]*eyes[0][3]
        area_eye_two = eyes[-1][2]*eyes[-1][3]
        area_diff = abs(area_eye_one-area_eye_two)
        eye_list.append([abs(degrees),area_diff,eyes[0],eyes[-1]])
        eye_list.sort()
        i=0

        #REMOVING EYE COMBOS WITH ANGLES > 30
        while i < len(eye_list):
            #If the angle of the two eye pairs are greater than 30, it is not an eye
            if eye_list[i][0] > 15: 
                eye_list.pop(i)
            else:
                i+=1
        
        #Sorting Eye Combos by the most similar size
        eye_list.sort(key = lambda x: x[1])
        selected_eyes = eye_list[0]

        #removing angle and area diffs
        selected_eyes.pop(0)
        selected_eyes.pop(0)
        return selected_eyes

 #If < 2 eyes detected, attempt to get them by identifying circles in image.
    if len(eyes) < 2:
        gray_blurred = cv2.blur(gray, (5, 5))
        # Apply Hough transform on the blurred image.
        eyes = cv2.HoughCircles(gray_blurred, 
                           cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                       param2 = 30, minRadius = 15 , maxRadius = 50 )
        if eyes is not None:
            # Convert the circle parameters a, b and r to integers.
            eyes = np.uint16(np.around(eyes))
            i=0
            eyes = eyes[0]
            while i < len(eyes)-1:
                eye_one = eyes[i]
                eye_two = eyes[i+1]
                eye_one_radius = eyes[i][2]
                eye_two_radius = eyes[i+1][2]
                area_diff = abs(eye_one_radius-eye_two_radius)
                degrees = get_degrees(eye_one,eye_two)
                eye_list.append([abs(degrees),area_diff,eye_one, eye_two])
                print("DEGREES:",degrees)
                i+=1
            degrees = get_degrees(eyes[0],eyes[-1])

            eye_one_rad = eyes[0][2]
            eye_two_rad = eyes[-1][2]
            area_diff = abs(eye_one_rad-eye_two_rad)
            eye_list.append([abs(degrees),area_diff,eyes[0],eyes[-1]])
            eye_list.sort()
            i=0

        #REMOVING EYE COMBOS WITH ANGLES > 30
        i=0
        while i < len(eye_list):
            if eye_list[i][0] > 15:
                eye_list.pop(i)
            else:
                i+=1
        #Sorting by pairs of eyes with most similar size
        eye_list.sort(key = lambda x: x[1])
        
        selected_eyes = eye_list[0]
        #removing angle and area diffs
        selected_eyes.pop(0)
        selected_eyes.pop(0)
        
        return selected_eyes



    #Two eyes found. Returning Eyes
    return eyes

def blur_eyes(face,eyes):
    ksize = (30,30)
    mask_face = np.zeros(face.shape, dtype='uint8')
    for eye in eyes:
        if len(eye) == 4:
            x,y,w,h = eye
            roi = face[y:y+h, x:x+w]
            roi = cv2.blur(roi, ksize, cv2.BORDER_DEFAULT) 
            face[y:y+h, x:x+w] = roi
        else:
            circle_center = (eye[0],eye[1])
            circle_radius= eye[2]
            cv2.circle(mask_face, circle_center, circle_radius, (255, 255, 255), -1)
            img_all_blurred = cv2.blur(face, ksize)
            face = np.where(mask_face > 0, img_all_blurred, face)
            view_img(face, "Blurred")
    return face

def display_image_list(image_title, imgs):
    fig = plt.figure(image_title,figsize=(20,7))
  
    rows = 1
    columns = len(imgs)

    j=1
    for img in imgs:
        height, width = img.shape[:2]
        fig.add_subplot(rows,columns,j)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(image_title + "_" + str(j))

        j+=1
    plt.show()

def process_image(img_file, expected_faces, face_cascade):
    img = cv2.imread(img_file)
    img_copy = img.copy()

    img_copy, faces = get_faces(img_copy, expected_faces, face_cascade)
    blurred_faces = []
    
    view_img(img_copy, "FACES DETECTED")

    for face in faces:
        x,y,w,h = face
        roi = img[y:y+h, x:x+w]

        view_img(roi, "Face")

        eyes = get_eyes(roi, face,img)
        rotated_face = rotate_face(eyes[0], eyes[1], roi)
        blurred_eyes = blur_eyes(rotated_face,eyes)

        view_img(blurred_eyes, "Blurred Face")
        blurred_faces.append(blurred_eyes)
    return blurred_faces, img_copy

def main():
    images=[]

    img_file = "Image1_MultipleSubjects.jpg"
    expected_faces = 2
    face_cascade = cv2.CascadeClassifier('C:\opencv\haarcascades\haarcascade_frontalface_alt_tree.xml')
    faces, img = process_image(img_file, expected_faces, face_cascade)
    display_image_list("Image 1 - Face ",faces)
    images.append(img)

    img_file = "Image2-SubjectFarAway.jpg"
    expected_faces = 1
    face_cascade = cv2.CascadeClassifier('C:\opencv\haarcascades\haarcascade_frontalface_alt_tree.xml')
    faces, img = process_image(img_file, expected_faces, face_cascade)
    display_image_list("Image 2 - Face ",faces)               
    images.append(img)

    img_file = "Image3_NonHuman.jpg"
    expected_faces = 1
    face_cascade = cv2.CascadeClassifier('C:\opencv\haarcascades\haarcascade_frontalcatface.xml')
    faces, img = process_image(img_file, expected_faces, face_cascade)
    display_image_list("Image 3 - Face ", faces)
    images.append(img)

    display_image_list("Image", images)
    pass

if __name__ == '__main__' : main()
