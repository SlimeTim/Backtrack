from tkinter import *
from tkinter import ttk
from Define import *
import random

# Biến global 
global answer,route,tabaleData,bestRoute, cityMap

root = Tk()

# Thiết kế khung hiển thị giao diện
root.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT,WINDOW_POSITION_RIGHT,WINDOW_POSITION_DOWN))

#Khung chứa toàn bộ nội dung 
rootFrame = Frame(root, bg='gray94')
rootFrame.grid(row=1,column=0,sticky=NW)

# Tạo một khung chứa thanh cuộn
frame = ttk.Frame(rootFrame)
frame.grid(row=0, column=0)

# Tạo một thanh cuộn dọc
verticalScrollbar = ttk.Scrollbar(frame, orient="vertical")
verticalScrollbar.grid(row=0, column=1, sticky="ns")

# Tạo một thanh cuộn ngang
horizonScrollbar = ttk.Scrollbar(frame, orient="horizontal")
horizonScrollbar.grid(row=1, column=0, sticky="ew")

# Tạo một lưới để điền nội dung
canvas = Canvas(frame, height= 580, width=780,bg = "#DAF7A6",yscrollcommand=verticalScrollbar.set, xscrollcommand=horizonScrollbar.set)
canvas.grid(row=0, column=0, sticky="nsew")

# Kết nối thanh cuộn với khung
verticalScrollbar.config(command=canvas.yview)
horizonScrollbar.config(command=canvas.xview)

# Tạo một khung bên trong canvas để đặt nội dung cuộn
inner_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw",height=5000,width=5000)

# Thiết kế 
root.title("BÀI TOÁN DU LỊCH")

editFrame = Frame(inner_frame, bg='gray94')
editFrame.grid(row = 0, column = 0, columnspan = 3,sticky=W)

mainLabel = Label(editFrame, text="BÀI TOÁN DU LỊCH", font=10)
mainLabel.grid(row= 0, columnspan=3,sticky="nsew")

# Thiết lable vs text cho số lượng thành phố 
NumCityLabel = Label(editFrame, text="Nhập số lượng thành phố n   = ",font="10")
NumCityLabel.grid(row = 1, column = 0)

NumCityText = Text(editFrame, height = 1, width = 5,insertbackground="blue")
NumCityText.grid(row = 1, column = 1, sticky=W)

NumCityLabel_root = Label(editFrame, text="")
NumCityLabel_root.grid(row = 1, column = 2,sticky=W)


# Thiết kế button Next sau khi đã nhập dữ liệu vào 
NextButton = Button(editFrame, text= "NEXT",bg="#DAF7A6",height = 2, width = 12, command=lambda: SetCityMapTable(NumCityText.get(0.0,END)))
NextButton.grid(row = 2, column = 1, sticky= S)

#Tạo một Frame cho bảng
tableFrame = Frame(inner_frame, bg='gray94')
tableFrame.grid(row=1, column=0, columnspan=3, sticky=NW)

entryWidget = []  # Lưu trữ các widget Entry

# Thiết lập một bảng danh sách các thành phố
def SetCityMapTable(n):
        if NumCityText.get(0.0, "end-1c").isdigit():
          # Kiểm tra xem giá trị là một số
          NumCityLabel_root.config(text=f" n = {NumCityText.get(0.0, 'end-1c')}", font=("Arial", 12))
          n = int(n)
        else:
          # Nếu giá trị không phải số, hiển thị thông báo
          NumCityLabel_root.config(text="Hãy nhập vào một số !!", font=("Arial", 16))

        # Xóa các widget hiện tại trong root
        for widget_row in entryWidget:
            for widget in widget_row:
                widget.destroy()

        entryWidget.clear()  # Xóa danh sách widget hiện tại

        for i in range(n+1):
            rowEntry = []  # Lưu trữ các Entry trong một hàng
            for j in range(n+1):
                table = Entry(tableFrame, width=8, fg='blue', font=('Arial', 12, 'bold'))
                table.grid(row=i, column=j)
                row = i
                column = j
                if(row == 0 and column == 0):
                     table.insert(END,"CITIES")
                     rowEntry.append(table)
                elif(row == 0 and column > 0):
                     table.insert(END,f"city {j}")
                     rowEntry.append(table)
                elif(row > 0 and column == 0):
                     table.insert(END,f"city {i}")
                     rowEntry.append(table)
                elif(row == column):
                     table.insert(END,f"{0}")
                     rowEntry.append(table)
                     table.config(state=DISABLED)
                elif(row < column):
                     table.insert(END,f"")
                     table.config(state=DISABLED)
                else:
                     table.insert(END,"")
                     rowEntry.append(table)   
                table.config(justify=CENTER)  
            entryWidget.append(rowEntry)  
        GetCityMapButton.grid(row = n+1, column = 2)
        RandomCityMapButton.grid(row = n+1, column= 1)

# Button Get và Random 
GetCityMapButton = Button(tableFrame, text = "GET",bg="#DAF7A6", height = 1, width = 8, command=lambda:getCityMap(NumCityText.get(0.0,END), False))

RandomCityMapButton = Button(tableFrame, text = "RANDOM",bg="#FFC300",height = 1, width = 8, command=lambda:randomCityMap(NumCityText.get(0.0,END)),)


def randomCityMap(n):
     n = int(n)
     entryWidget.clear()
     entry = []
     for i in range(n+1):
          rowdata = []
          for j in range(n+1):
               rand = random.randint(0,100)
               rowdata.append(rand)
          entry.append(rowdata)

     for i in range(n+1):
          for j in range(n+1):
               if(i>0 and j>0):
                    if(j > i):
                         entry[i][j] = entry[j][i]
          entryWidget.append(entry[i])
     
     getCityMap(NumCityText.get(0.0,END), True)

     

# Thiết lập một table items là dữ liệu sau khi sort từ bảng dữ liệu ban đầu 
def getCityMap(n, isRandom):
        n = int(n)
        global tableData
        tableData = []
        for i in range(n+1):
            rowData = []  # Dữ liệu từ một hàng
            for j in range(n+1):
                if( i>0 and j >0):
                    if(i >= j):
                         entry = entryWidget[i][j]
                    elif(i<j):
                         entry = entryWidget[j][i]
                    if(isRandom):
                         value = entry
                    else:
                         value = entry.get()  # Lấy giá trị từ Entry
                    rowData.append(value)
            tableData.append(rowData)   
        
        entryWidget.clear()
        tableData.remove([])

        for i in range(n+1):
            rowEntry = []
            for j in range(n+1):
                table = Entry(tableFrame, width=8, fg='blue', font=('Arial', 12, 'bold'))
                table.grid(row=i, column=j)
                row = i
                column = j
                if(row == 0 and column == 0):
                     table.insert(END,"CITIES")
                     rowEntry.append(table)
                elif(row == 0 and column > 0):
                     table.insert(END,f"city {j}")
                     rowEntry.append(table)
                elif(row > 0 and column == 0):
                     table.insert(END,f"city {i}")
                     rowEntry.append(table)
                elif(row == column):
                     table.insert(END,f"{0}")
                     rowEntry.append(table)
                else:
                     table.insert(END,f"{tableData[i-1][j-1]}")
                     rowEntry.append(table) 
                if(not isRandom):
                    tableData[i-1][j-1] = int(tableData[i-1][j-1])
                table.config(state=DISABLED)  
                table.config(justify=CENTER)  
            entryWidget.append(rowEntry)
        firstCityLabel.grid(row = 0, column = 0)
        firstCityText.grid(row = 0, column = 1, sticky=W)
        firstCityLabel_root.grid(row = 0, column = 2,sticky=W)
        firstCityButton.grid(row = 1, column= 1)


# Tạo một Frame cho Solve Problem
solveFrame = Frame(inner_frame, bg='gray94')
solveFrame.grid(row=3, column=0, columnspan=6, sticky=NW) 

firstCityLabel = Label(solveFrame, text="Nhập thành phố khởi đầu:  ",font="10")

firstCityText = Text(solveFrame, height = 1, width = 5,insertbackground="blue")

firstCityLabel_root = Label(solveFrame, text="")


firstCityButton = Button(solveFrame, text="NEXT",bg="#DAF7A6",width= 12, command=lambda:Remap(NumCityText.get(0.0,END), firstCityText.get(0.0,END)))


def Remap(n, beginCity):
     n = int(n)
     if (firstCityText.get(0.0,'end-1c').isdigit() and int(firstCityText.get(0.0,'end-1c'))<=n and int(firstCityText.get(0.0,'end-1c'))>0):
          # Kiểm tra xem giá trị là một số
          firstCityLabel_root.config(text=f" Begin City = {firstCityText.get(0.0, 'end-1c')}", font=("Arial", 12))
          beginCity= int(beginCity) - 1
          canSolve = True
     else:
          # Nếu giá trị không phải số, hiển thị thông báo
          firstCityLabel_root.config(text=f"Hãy nhập vào một số >0 vaf <={n} !!", font=("Arial", 12))
          canSolve = False

     n = int(n)
     beginCity = int(beginCity)
     global cityMap
     cityMap = [0 for i in range(n)]
     for i in range(0, n - beginCity):
          cityMap[i] = tableData[i+beginCity]
     for j in range(n - beginCity, n):
          cityMap[j] = tableData[j - beginCity]

     if(canSolve):
          solveButton.grid(row = 2, column=1)

solveButton = Button(solveFrame, text="SOLVE",font=12, width= 14,bg="#FF5733", command= lambda:Solve(NumCityText.get(0.0,END), firstCityText.get(0.0,END)))

def Solve(n, beginCity):
     n =int(n)
     beginCity = int(beginCity) - 1
     global answer, route,result, bestRoute
     answer = [99999999]
     route = [0 for i in range(n+1)]
     result = []
     bestRoute = []
     passedCity = [False for i in range(n+1)]
     passedCity[0] = True

     Backtracking(cityMap, passedCity, 0, n, 1, 0)
     realRoute(n, beginCity)

     cityRoute = ""
     for i in range(len(bestRoute)-1):
          cityRoute += f"{bestRoute[i]+1} -> "
     cityRoute += f"{beginCity+1}"

     answerLabel = Label(answerFrame,text=f"Quãng đường ngắn nhất:   {min(answer)}", font = 16,padx=50, pady=10)
     routeLabel = Label(answerFrame,text=f"Thứ tự thành phố: {cityRoute}", font = 16, padx=50, pady = 10)

     answerLabel.grid(row = 3, sticky=W)
     routeLabel.grid(row = 4, sticky=W)

def Backtracking(cityMap, passedCity, currCity, n, count, cost):
     global answer, route, result, bestRoute
     costTemp = cost + cityMap[currCity][0]
     if (count == n and cityMap[currCity][0] and costTemp < min(answer)):
          answer.append(costTemp)
          
          if(len(bestRoute) >= n):
               bestRoute.clear()
               bestRoute.extend(route)
          else:
               bestRoute.extend(route)
          return
     for i in range(n):
          if (passedCity[i] == False and cityMap[currCity][i]):
               route[count] = i
               passedCity[i] = True
               Backtracking(cityMap, passedCity, i, n, count + 1,
               cost + cityMap[currCity][i])
               passedCity[i] = False     
def realRoute(n, beginCity):
  global bestRoute
  for i in range(len(bestRoute)):
    if((bestRoute[i] + beginCity) < n):
      bestRoute[i]+= beginCity
    else:
      bestRoute[i] += beginCity-n

answerFrame = Frame(inner_frame, bg='gray94')
answerFrame.grid(row=4, column=0, columnspan=6, sticky=NW) 


#Cài đặt khả năng cuộn
inner_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()