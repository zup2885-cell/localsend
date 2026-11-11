import AppKit
import Foundation
let base = URL(fileURLWithPath: CommandLine.arguments[1])
func render(_ size: Int, _ color: NSColor, _ duplicate: Bool) -> Data {
    let bitmap = NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:size,pixelsHigh:size,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep:bitmap)
    let n=CGFloat(size)
    color.setFill(); NSBezierPath(roundedRect:NSRect(x:0,y:0,width:n,height:n),xRadius:n*0.22,yRadius:n*0.22).fill()
    NSColor.white.withAlphaComponent(0.35).setStroke()
    let back=NSBezierPath(roundedRect:NSRect(x:n*0.22,y:n*0.31,width:n*0.4,height:n*0.44),xRadius:n*0.045,yRadius:n*0.045);back.lineWidth=n*0.037;back.stroke()
    NSColor.white.setStroke()
    let front=NSBezierPath(roundedRect:NSRect(x:n*0.37,y:n*0.19,width:n*0.4,height:n*0.44),xRadius:n*0.045,yRadius:n*0.045);front.lineWidth=n*0.037;front.stroke()
    let arrow=NSBezierPath();arrow.lineWidth=n*0.04;arrow.lineCapStyle = .round;arrow.lineJoinStyle = .round
    if duplicate {arrow.move(to:NSPoint(x:n*0.48,y:n*0.4));arrow.line(to:NSPoint(x:n*0.55,y:n*0.33));arrow.line(to:NSPoint(x:n*0.68,y:n*0.49))}
    else {arrow.move(to:NSPoint(x:n*0.46,y:n*0.4));arrow.line(to:NSPoint(x:n*0.68,y:n*0.4));arrow.move(to:NSPoint(x:n*0.6,y:n*0.49));arrow.line(to:NSPoint(x:n*0.69,y:n*0.4));arrow.line(to:NSPoint(x:n*0.6,y:n*0.31))}
    arrow.stroke();NSGraphicsContext.restoreGraphicsState()
    return bitmap.representation(using:.png,properties:[:])!
}
for (name,color,duplicate) in [("quick",NSColor(calibratedRed:0.08,green:0.36,blue:0.43,alpha:1),false),("dedup",NSColor(calibratedRed:0.29,green:0.26,blue:0.55,alpha:1),true)] {
    let dir=base.appendingPathComponent(name+".iconset");try FileManager.default.createDirectory(at:dir,withIntermediateDirectories:true)
    for size in [16,32,64,128,256,512,1024] {try render(size,color,duplicate).write(to:dir.appendingPathComponent("icon_\(size)x\(size).png"))}
}
