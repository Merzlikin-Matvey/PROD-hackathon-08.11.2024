"use client";
import React, { useEffect, useState } from "react";
import TourCard from "./tour_card";
import "./styles.css";
import selected_pin from "../../public/pin.png";
import pie from "../../public/pie.png";
import person from "../../public/person.png";
import { fetchTours } from "../api";
import Link from "next/link";
import "./bar.css"

interface Tour {
  name: string;
  start_date: string;
  end_date: string;
  country: string;
}

export default function Home() {
  const [tours, setTours] = useState<Tour[]>([]);

  useEffect(() => {
    async function loadTours() {
      try {
        const toursData = await fetchTours();
        setTours(toursData);
      } catch (error) {
        console.error("Failed to fetch tours:", error);
      }
    }
    loadTours();
  }, []);

  return (
      <div>
        <div className="bg_3">
          <a id="title">Мероприятия</a>
          <div className="bg_4"></div>
        </div>

        <div id="tours">
          <div className="tours-header">
            <a id="your-events">Ваши мероприятия:</a>
            <Link href="/add-tour" id="add-tour-button">
              <button id="create-event">Создать мероприятие</button>
            </Link>
          </div>
          <br/>
          {tours.map((tour, index) => (
              <TourCard
                  key={index}
                  title={tour.name}
                  startDate={tour.start_date}
                  endDate={tour.end_date}
                  description={tour.country}
              />
          ))}
        </div>

        <div id="bar">
          <img src={selected_pin.src} alt="Pin" className="selected_bar_img"/>
          <img src={pie.src} alt="Pie" className="bar_img"/>
          <img src={person.src} alt="Person" className="bar_img"/>
        </div>
      </div>
  );
}