import Foundation

public struct Point {
    var x: Int
    var y: Int
    public init(x: Int, y: Int) {
        self.x = x
        self.y = y
    }
    public func getX() -> Int {
        return self.x
    }
    public func getY() -> Int {
        return self.y
    }
}
