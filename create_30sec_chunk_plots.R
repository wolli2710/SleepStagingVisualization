positions = c("_mattrass", "_right_arm")
vps = c(26,27,28,29,30,31)
ppi = 300


for(pos in positions){
    for(vp in vps){
        fileData <- read.csv(paste("result_data_vp", vp, pos, "/VP", vp, pos, "_30sec_chunks.csv", sep=""), header=TRUE, skip=1)

        png(file=paste("result_data_vp", vp, pos, "/VP", vp, pos, "_30sec_chunks.png", sep=""), height=3508, width=2480)
        colors <- c(rgb(0,0,1),rgb(0.75,0,0.25))

        split.screen( figs = c( 5, 1 ) )

        split.screen( figs = c( 1,1 ), screen = 1 )
        split.screen( figs = c( 1,1 ), screen = 2 )
        split.screen( figs = c( 1,1 ), screen = 3 )
        split.screen( figs = c( 1,1 ), screen = 4 )
        split.screen( figs = c( 1,1 ), screen = 5 )

        screen(1)
        par(mar=c( 5, 12, 7, 10 ), mgp=c(4,2,0.2))
        plot( c(fileData[,1]), type="l", col=colors[1], col.lab="palegreen3" , xlab="30 sec slots", ylab="", ylim=c(0, 5), lwd=5, 
            main=paste("VP", vp, pos, sep=""), cex.main=5, cex.lab=3.5, cex.axis=3, las=1)
        title(ylab="sleep stages",mgp=c(-3,1,0), cex.lab=3.5, col.lab="palegreen3")
        legend("topleft", inset=.05, title="", c("Sleep Stage") , fill=colors, cex=2.5)

        screen(2)
        par(mar=c( 5, 12, 7, 10 ), mgp=c(4,2,0.2))
        plot( c(fileData[,7]), type="l", col=colors[1], col.lab="palegreen3", xlab="30 sec slots", ylab="", ylim=c(0, 0.2), 
            lwd=5, cex.lab=3, cex.axis=3 , las=1)
        title(ylab="acceleration means",mgp=c(-3,1,0), cex.lab=3.5, col.lab="palegreen3")
        legend("topleft", inset=.05, title="", c("acceleration means") , fill=colors, cex=2.5)

        screen(3)
        par(mar=c( 5, 12, 7, 10 ), mgp=c(4,2,0.2))
        plot( c(fileData[,8]), type="l", col=colors[1], col.lab="palegreen3", xlab="30 sec slots", ylab="", ylim=c(0, 5.6), 
            lwd=5 , cex.lab=3, cex.axis=3 , las=1)
        title(ylab="acceleration max",mgp=c(-3,1,0), cex.lab=3.5, col.lab="palegreen3")
        legend("topleft", inset=.05, title="", c("acceleration max") , fill=colors, cex=2.5)


        screen(4)
        par(mar=c( 5, 12, 7, 10 ), mgp=c(4,2,0.2))
        plot( c(fileData[,3]), type="l", col=colors[1], col.lab="palegreen3", xlab="30 sec slots", ylab="", ylim=c(0, 40), 
            lwd=5 , cex.lab=3, cex.axis=3, las=1 )
        title(ylab="audio means",mgp=c(-3,1,0), cex.lab=3.5, col.lab="palegreen3")
        legend("topleft", inset=.05, title="", c("audio means") , fill=colors, cex=2.5)

        screen(5)
        par(mar=c( 5, 12, 7, 10 ), mgp=c(4,2,0.2))
        plot( c(fileData[,4]), type="l", col=colors[1], col.lab="palegreen3", xlab="30 sec slots", ylab="", ylim=c(0, 10000), 
            lwd=5 , cex.lab=3, cex.axis=3, las=1 )
        title(ylab="audio max",mgp=c(-3,1,0), cex.lab=3.5, col.lab="palegreen3")
        legend("topleft", inset=.05, title="", c("audio max") , fill=colors, cex=2.5)
        
        readline("Press <Enter> to continue")
    }
}