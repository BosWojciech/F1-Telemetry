import { store } from "./store";
// import all slices update methods

export const dispatchPacket = (packet: any) =>{
    const packetType = packet.header.packetId;

    switch(packetType){
        default:
            console.log("Unknown Packet")
    }
}