import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyCk2HherDx1DmOwG4lCOoZeApOstkwkQyc",
  authDomain: "campusguidegpt-93357.firebaseapp.com",
  projectId: "campusguidegpt-93357",
  storageBucket: "campusguidegpt-93357.firebasestorage.app",
  messagingSenderId: "951554938433",
  appId: "1:951554938433:web:e9524bfd7c522c190e18c0",
  measurementId: "G-6GQG8T8WLC"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);