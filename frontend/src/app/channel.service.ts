import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { WebSocketService } from './web-socket.service';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/filter';

const CHANNEL_URL = 'ws://localhost:8000/api/ws/';

export interface Message {
  stream: string;
  payload: object;
}

@Injectable()
export class ChannelService {
  public messages: Subject<Message>  = new Subject<Message>();

  constructor(private wsService: WebSocketService) {

    // 1. subscribe to chatbox
    this.messages   = <Subject<Message>>this.wsService
      .connect(CHANNEL_URL)
      .map((response: MessageEvent): Message => {
        let data = JSON.parse(response.data);
        return {
          stream : data.stream,
          payload : data.payload
        };
      });
  }
}