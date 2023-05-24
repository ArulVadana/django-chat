const APP_ID = APP_ID
const CHANNEL =sessionStorage.getItem('room')
const TOKEN = sessionStorage.getItem('token')

let UID = sessionStorage.getItem('UID')
let name = sessionStorage.getItem('name')


const client = AgoraRTC.createClient({mode:'rtc',codec:'vp8'})

let localTracks = []
let remoteUser={}

let joinAndDisplayLocalstream = async () => {

    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)

    try{
        UID = await client.join(APP_ID, CHANNEL, TOKEN, UID)
    }catch(error){
        console.error(error)
        window.open('/', '_self')
    }

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

    let player = `<div class="video-box" id="user-container-${UID}">
    <div class="video-player" id="user-${UID}"></div>
    <div class="name-wrapper"><span class="username">${name}</span></div> 
    </div>`

    document.getElementById('video-stream').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`)

    await client.publish([localTracks[0],localTracks[1]])

}

let handleUserJoined = async (user,mediaType) => {
    remoteUser[user.uid] = user
    await client.subscribe(user, mediaType)

    if (mediaType ==="video"){
        let player = document.getElementById(`user-container-${user.uid}`)
        if (player != null){
            player.remove()
        }
        
        let member=await getMember(user)
       

        player=  `<div class="video-box" id="user-container-${user.uid}">
        <div class="video-player" id="user-${user.uid}"></div>
        <div class="name-wrapper"><span class="username">${member.name}</span></div> 
        </div>`

        document.getElementById('video-stream').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)

    }

    if (mediaType==="audio"){
        user.audioTrack.play()
    }

}

let handleUserLeft = async (user) =>{
    delete remoteUser[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()

}

let leaveAndRemoveLocakstream = async () => {
    for(let i=0;localTracks.length >i;i++){
        localTracks[i].stop()
        localTracks[i].close()
    }
    await client.leave()

    deleteMember()
    window.history.back()
} 

let audioControl = async (e) => {
    if (localTracks[0].muted){
        await localTracks[0].setMuted(false)
        console.log(e.target)
        document.getElementById('voice-control').style.backgroundColor='#fff'
    }else{
        await localTracks[0].setMuted(true)
        console.log(e.target)
        document.getElementById('voice-control').style.backgroundColor='red'
    }
}

let videoControl = async (e) => {
    if (localTracks[1].muted){
        await localTracks[1].setMuted(false)
        
        document.getElementById('video-control').style.backgroundColor='#fff'
    }else{
        await localTracks[1].setMuted(true)
        
        document.getElementById('video-control').style.backgroundColor='red'
    }
}

let getMember = async (user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`)
    let member = await response.json()
    return member
}

let deleteMember = async () => {
    let response = await fetch('/delete_member/', {
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'name':name, 'room_name':CHANNEL, 'UID':UID})
    })
    let member = await response.json()
}

joinAndDisplayLocalstream()

document.getElementById('exit').addEventListener('click', leaveAndRemoveLocakstream)
document.getElementById('voice-control').addEventListener('click',audioControl)
document.getElementById('video-control').addEventListener('click',videoControl)