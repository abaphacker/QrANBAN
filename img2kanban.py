import cv2
import detectCards as dc

if __name__ == '__main__':
        img = cv2.imread("/home/harry/python_workspace/kanban2.jpg")
        cards = dc.getCards(img)
        i = 0
        for card in cards:
            i = i + 1
            filename = "/home/harry/python_workspace/cards/card%s.png" % i 
            card.highlight_card_in_img()
            card.save_img(filename)
        
        cv2.imwrite("/home/harry/python_workspace/cards/all_cards.png", img)
        cv2.imshow("QrANBAN", img)
        cv2.waitKey(0)
        
