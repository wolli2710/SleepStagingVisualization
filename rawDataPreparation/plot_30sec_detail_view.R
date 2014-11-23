# execute the script create_pre_processed_rawdata_files.py before plotting!!

secIndex = 125
vp = 26
pos = "_right_arm"
# pos = "_mattrass"
steps = 30 

hz = 500
startPoint = (secIndex*30*hz)
endPoint = (steps * hz)


labelStart = startPoint/1000
labelEnd = endPoint/1000

fileData <- read.csv( paste("/Users/wolli/Mac_Shared_Folder/python/MasterArbeit/rawDataPreparation/r_VP", vp, pos, "_output.csv", sep=""), header=TRUE, skip=startPoint, nrows=endPoint)

print(startPoint)
print( length(fileData[0]) )

max_y = 500 #max(fileData)
min_y = -300 #min(fileData)

colors <- c(rgb(1,0.5,1),
    rgb(0.75,0.5,0.25),
    rgb(1.0,0.0,0.0),
    rgb(0.0,1.0,0.0),
    rgb(0.0,0.0,1.0),
    rgb(1.0,1.0,0.0),
    rgb(0.0,1.0,1.0),
    rgb(0.5,0.5,0.5),
    rgb(0.5,0.0,0.0),
    rgb(0.0,0.5,0.0),
    rgb(0.0,0.0,0.5),
    rgb(1,0.6,0.4),
    rgb(1,0.8,0.2),
    rgb(0.9,0.25,0.9),
    rgb(0.8,0.8,0.2),
    rgb(0.6,0.4,1),
    rgb(0.6,1,0.7),
    rgb(0.75,0.0,1.0),
    rgb(0.9,0.25,0.65),
    rgb(0.75,0.75,0.75),
    rgb(0.75,0.0,0.0),
    rgb(0.0,0.75,0.0),
    rgb(0.0,0.0,0.75),
    rgb(0.75,0.75,0.0),
    rgb(0.0,0.75,0.75),
    rgb(0.0,0.0,0.0))

png(file=paste("VP", vp,"_", secIndex, ".png", sep=""), height=1080, width=1920)
par(mar=c( 4, 12, 7, 10 ), mgp=c(2,2,0.2))
plot( c(fileData[,1]), xlab="30 sec", ylab="Value", type="l", col=colors[1], ylim=c(min_y, max_y), cex.lab=1.5, axes=FALSE)
for(i in 1:26){
    lines( c(fileData[,i]), type="l", col=colors[i])
}
axis(1, at=c(0,15000), labels=c( 0, 30 ), srt=60, tck=0.01, lwd.ticks=0.1, cex.axis= 1.5)
axis(2, cex.axis= 1.5)
data = c("F3","Fz","F4","Fc3","Fc4","C3","Cz","C4","Cp5","Cpz","Cp6","P3","Pz","P4","A1","A2","HEOGL","HEOGR","VEOGup","VEOGdown","EMGL","EMGR","ECG1","ECG2","acceleration","audio")     
legend("topleft", inset=.05, title="Channels", data, fill=colors, ncol=3, cex=2.0)
title(main=paste("VP", vp, "_",secIndex, sep=""), cex.main=3, font.main=4)

readline("Press <Enter> to continue")