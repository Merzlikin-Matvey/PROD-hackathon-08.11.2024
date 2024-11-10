"use client";
import React, { useEffect, useState } from "react";
import EventBlock from "./event_block";
import Link from "next/link";
import "./style.css";

const EventsPage: React.FC = () => {
  const [tourUuid, setTourUuid] = useState<string | null>(null);
  // eslint-disable-next-line
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    const uuid = new URLSearchParams(window.location.search).get("tour_uuid");
    setTourUuid(uuid);
    if (uuid) {
      fetchEvents(uuid);
    }
  }, []);

  const fetchEvents = async (uuid: string) => {
    try {
      const response = await fetch(`/api/events?tour_uuid=${uuid}`);
      if (response.ok) {
        const data = await response.json();
        setEvents(data.events);
      } else {
        console.error("Failed to fetch events");
      }
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  };
  // eslint-disable-next-line
  const handleUpdateEvent = async (updatedEvent: any, index: number) => {
    try {
      const response = await fetch(`/api/update_event`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ...updatedEvent, tour_uuid: tourUuid }),
      });
      if (response.ok) {
        alert("Мероприятие успешно обновлено!");
        if (tourUuid) {
          fetchEvents(tourUuid);
        }
      } else {
        alert("Ошибка при обновлении мероприятия.");
      }
    } catch (error) {
      console.error("Error updating event:", error);
      alert("Ошибка при обновлении мероприятия.");
    }
  };

  return (
      <div className="events-page">
        <Link href={`/add-event?tour_uuid=${tourUuid}`}>
          <button className="add-event-button">Добавить мероприятие</button>
        </Link>
        {events.map((event, index) => (
            <div key={index}>
              <EventBlock
                  uuid={event.uuid}
                  title={event.name}
                  startDate={event.start_date}
                  endDate={event.end_date}
                  data={JSON.parse(event.event_data)}
                  onUpdate={(updatedEvent) => handleUpdateEvent(updatedEvent, index)}
              />
            </div>
        ))}
      </div>
  );
};

export default EventsPage;