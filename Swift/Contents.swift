import Cocoa

//let data = ["apples": 10, "oranges": 15, "lemons": 5, "limes": 20]
//let names = Array(data.keys) //without array it's not an array it's some weird dict type
//let b = names
//print(names)


// 1. Reading data from file
let fileURL = Bundle.main.url(forResource: "AEMwithSpace", withExtension: "txt")
let content = try String(contentsOf: fileURL!, encoding: String.Encoding.utf8)

// 2. Changing data from single string into two arrays of x and y values
let stringArray = content.components(separatedBy: CharacterSet.decimalDigits.inverted)
var xArray: [Int] = []
var yArray: [Int] = []
var elementGroup: [Int] = []
var counter = 0
// spliting data into two arrays
for item in stringArray {
    if let number = Int(item) {
        if counter == 0 {
            //do nothing
            // it's index number which I won't use because of list is indexed
        } else if counter == 1 {
            xArray.append(number)
        } else if counter == 2 {
            yArray.append(number)
        } else if counter == 3 {
            elementGroup.append(number)
        }
    }
    if counter < 4 {
        counter += 1
    } else {
        counter = 0
    }
}
//print(xArray)
//print(yArray)
// 3. Creating Point struct and using it for creating array of Points which holds x,y values
// Tego z tym punktem nie używam w sumie(to od starego kodu) teraz tylko tworzę grupy niżej i tam są tworzone punkty
var listOfPoints: [Point] = []

if xArray.count == yArray.count && xArray.count == elementGroup.count { // xArray and yArray should be equal lengths (it would be nicer to change this into a function later and use guard statement)
    for index in 0..<xArray.count {
        let newPoint = Point(x: xArray[index], y: yArray[index])
        listOfPoints.append(newPoint)
    }
}
//print(listOfPoints)


var groups = [Group(groupNumber: 0, groupPoints: []),
            Group(groupNumber: 1, groupPoints: []),
            Group(groupNumber: 2, groupPoints: []),
            Group(groupNumber: 3, groupPoints: []),
            Group(groupNumber: 4, groupPoints: []),
            Group(groupNumber: 5, groupPoints: []),
            Group(groupNumber: 6, groupPoints: []),
            Group(groupNumber: 7, groupPoints: []),
            Group(groupNumber: 8, groupPoints: []),
            Group(groupNumber: 9, groupPoints: [])]


//print(elementGroup)
func fillGroups(xArray: [Int], yArray: [Int], elementsGroup: [Int]) { // najlepiej zmienić później na lambdę

    for index in 0..<xArray.count {
        let currentIteratedPoint = Point(x: xArray[index], y: yArray[index])
        groups[elementsGroup[index]].groupPoints.append(currentIteratedPoint)
    }
}
fillGroups(xArray: xArray, yArray: yArray, elementsGroup: elementGroup)
print(groups)


// wybierz random z grupy(od 0 do group[0].groupPoints.count - 1)
func createTree(group: Group) {
    let firstElementIndex = Int.random(in: 0..<group.groupPoints.count)
    var unusedElements: [Point] = [] //index numbers are important so don't delete points just make them empty
    for point in group.groupPoints {
        unusedElements.append(point)
    }
    let firstElement = unusedElements[firstElementIndex]
    //unusedElements[firstElementIndex] = Point(x: -1, y: -1) // w ten sposób oznaczam że element jest pusty // jednak nie wywalam je potem po prostu
    unusedElements.remove(at: firstElementIndex)
    print("First \(firstElement)")
    
    
    // potrzebna będzie lista pozostałych elementów o długości groupPoints.count D
    // do jej utworzenia przejedziemy po wszystkich elementach oprócz elementu wylosowanego D
    // będziemy wiedzieć który jest wylosowany dzięki jego indeksowi
    // lista odległości musi składać się z odległości do punktów oraz ich indeksów D/N
    // po stworzeniu listy sprawdzamy któy element jest najmniejszy i tworzymy do niego połączenie(print nazwa el1 do el2)
    
   
    let listOfDistances = createDistanceList(for: firstElement, with: unusedElements)
    var smallestDistanceBuffer = listOfDistances[0]
    var unusedElementIndex = 0
    var smallestElementIndex = 0
    for distance in listOfDistances { //tu jest nadmiarowe jedno przejście dla pierwszego elementu
        if distance < smallestDistanceBuffer {
            smallestDistanceBuffer = distance
            smallestElementIndex = unusedElementIndex
        }
        unusedElementIndex += 1
    }
    
    //print(unusedElements[smallestElementIndex])
    var distInd: (Double, Int)
    distInd = smallestDistanceForElement(for: firstElement, with: unusedElements)
    
//    print("dist: \(distInd.0) element: \(unusedElements[distInd.1])")
    
    var elementsUsed: [Point] = []
    elementsUsed.append(firstElement)
    
    while(unusedElements.count != 0) { //zmień to na 0 to po prostu test póki co
        
        let listOfDistances = createDistanceList(for: firstElement, with: unusedElements)
        var smallestDistance = listOfDistances[0]
        var smallestPointIndex = 0
        var smallestElementIndex = 0 //this is one level deeper than PointIndex
        var elementIndex = 0
        for element in elementsUsed { //tutaj jeden raz za dużo przechodzę przez listę elementów nie przeszkadza ale nadmiarowe jest
            
            distInd = smallestDistanceForElement(for: element, with: unusedElements)
            if distInd.0 < smallestDistance {
                smallestDistance = distInd.0
                smallestElementIndex = distInd.1
                smallestPointIndex = elementIndex //confusing names change later
            }
            elementIndex += 1
            
        }
        //print("\(unusedElements[smallestElementIndex]) is added to tree for \(elementsUsed[smallestPointIndex]) with distance \(smallestDistance)") // do czego był unusedElementIndex?
       print("\(unusedElements[smallestElementIndex].getX()) \(unusedElements[smallestElementIndex].getY()) \(elementsUsed[smallestPointIndex].getX()) \(elementsUsed[smallestPointIndex].getY()) \(smallestDistance) ")
        
        elementsUsed.append(unusedElements[smallestElementIndex])
        unusedElements.remove(at: smallestElementIndex)
    }
    
    //Dodaj jeszcze jedną listę≥ używanych elementów i to dla niej wykonuj pętlę która skończy się gdy wszystkie nieużywane elementy się skończą, lista ta na początku mam mieć element wybrany losowo musi printować też dla jakiego elementu jest dobierany inny element.
    
    
    // W kolejnym kroku tworzymy listę dla kolejnego elementu i jego odległości do wszystkich elementów poza elementami których indeksy są wykorzystane(czyli ten element, wybrany losowo element(i dla kolejnych kroków poprzedni element) może najłatwiej byłoby na początku zrobić listę elementów które zostały już wykorzystane i wywalać z niej gsy ona będzie pusta wtedy zakończyć działanie algorytmu. Zrobić to w pętli for która wykonuje się tak długo aż ta lista nie będzie pusta. A w środku wywoływać listy/tą funkcję? aż się nie skończy
}
func smallestDistanceForElement(for element: Point, with unusedElements: [Point]) -> (Double, Int) {
    let listOfDistances = createDistanceList(for: element, with: unusedElements)
    var smallestDistanceBuffer = listOfDistances[0]
    var unusedElementIndex = 0
    var smallestElementIndex = 0
    for distance in listOfDistances { //tu jest nadmiarowe jedno przejście dla pierwszego elementu
        if distance < smallestDistanceBuffer {
            smallestDistanceBuffer = distance
            smallestElementIndex = unusedElementIndex
        }
        unusedElementIndex += 1
    }
    return (smallestDistanceBuffer, smallestElementIndex)
}

func createDistanceList(for point: Point, with unusedElements: [Point]) -> [Double] {
    var listOfDistances: [Double] = []
    for element in unusedElements {
        let distance = countDistance(from: point, to: element)
        listOfDistances.append(distance)
    }
    return listOfDistances
}

func countDistance(from sourcePoint: Point, to destinationPoint: Point) -> Double { //to other points
    let sourcePointX = Double(sourcePoint.getX())
    let sourcePointY = Double(sourcePoint.getY())
    let destinationPointX = Double(destinationPoint.getX())
    let destinationPointY = Double(destinationPoint.getY())
    let distance = sqrt(pow(destinationPointX - sourcePointX, 2) + pow(destinationPointY - sourcePointY, 2))
    return distance
}

// potem operując na tym randomie wylicz odległość do pozostałych punktów z grupy zapisując jaka była najmniejsza i dla jakiego elementu czyli na dwa bufory
// potem jeszcze raz to samo ale dla więcej niż jednego elementu(czyli powinieneś zapisać wszystkie odległości do elementów dla pierwszego elementu i zrobić kolejną listę odległości dla kolejnego elementu i porównać gdzie jest mniejsza tam gdzie mniejsza dodać element stworzyć dla niego nową listę i wywalić go ze starej listy) algorytm wykonuje się tak długo aż skończą się elementy na liście
func createTrees(for groups: [Group]) {
    var groupNumber = 0
    for group in groups {
        print("For group number \(groupNumber)")
        createTree(group: group)
        groupNumber += 1
    }
}

//createTree(group: groups[0])
createTrees(for: groups)

// na koniec powtórz dla wszystkich grup

