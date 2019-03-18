import Foundation

public struct Group {
    let groupNumber: Int
    public var groupPoints: [Point]
    public init(groupNumber: Int, groupPoints: [Point]) {
        self.groupNumber = groupNumber
        self.groupPoints = groupPoints
    }
}
