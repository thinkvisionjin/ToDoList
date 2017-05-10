import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { User } from '../user';
import {isSuccess} from "@angular/http/src/http_utils";

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {
  errors: {string: any};
  isSuccess = false;
  user: User;

  username;
  email;
  password1;
  password2;

  constructor(private authService: AuthService) {
    this.authService.user.subscribe(user => this.user = user);
    // this.authService.errors.subscribe(errors => this.errors = errors);
  }

  ngOnInit() {
  }

  registerUser() {
    this.authService.registerUser(this.username, this.email, this.password1, this.password2)
      .subscribe(data => {
        this.isSuccess = true;
      }, error => {
        this.errors = error.json();
      });
      // .then(response => {
      //     this.isSuccess = true;
      //   }, error => {
      //     this.errors = error.json();
      //   });
  }
}
