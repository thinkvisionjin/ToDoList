import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/do';

import { User } from './user';

@Injectable()
export class AuthService {
  private authUrl = '/api/web/';
  private _user: BehaviorSubject<User> = new BehaviorSubject<User>(null);

  constructor(private http: Http) {
    const url = `${this.authUrl}user/`;
    this.http.get(url)
      .subscribe(data => {
        this._user.next(data.json());
      });
  }

  get user() {
    return this._user.asObservable();
  }

  login(payload: {string: string}) {
    const url = `${this.authUrl}login/`;
    return this.http.post(url, payload)
      .do(res => {
        this._user.next(res.json());
      });
  }

  logout() {
    const url = `${this.authUrl}logout/`;
    return this.http.post(url, {})
      .do(res => {
        this._user.next(null);
      });
  }

  passwordReset(payload: {string: string}) {
    const url = `${this.authUrl}password/reset/`;
    return this.http.post(url, payload);
  }

  passwordResetConfirm(payload: {string: string}) {
    const url = `${this.authUrl}password/reset/confirm/`;
    return this.http.post(url, payload);
  }

  registerUser(payload: {string: string}) {
    const url = `${this.authUrl}registration/`;
    return this.http.post(url, payload)
      .do(response => {
        this._user.next(response.json());
      });
  }

  accountConfirmEmail(key: string) {
    const url = `${this.authUrl}registration/verify-email/`;
    return this.http.post(url, {key: key});
  }
}
