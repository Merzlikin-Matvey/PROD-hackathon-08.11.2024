"use client";
import React, { useState } from "react";
import "./style.css";
import { useRouter } from "next/navigation";

export default function AddEvent() {
  const [name, setName] = useState("");
  const [eventType, setEventType] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [eventData, setEventData] = useState("");
  const [flightNumber, setFlightNumber] = useState("");
  const router = useRouter();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const uuid = new URLSearchParams(window.location.search).get("tour_uuid");
    const eventDataObj: Record<string, string> = { место: eventData };
    if (eventType === "flight") {
      eventDataObj["flight_number"] = flightNumber;
    }
    const data: Record<string, unknown> = {
      name,
      tour_uuid: uuid,
      event_type: eventType,
      start_date: startDate,
      end_date: endDate,
      event_data: JSON.stringify(eventDataObj)
    };
    const response = await fetch("/api/add_event", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    if (response.ok) {
      alert("Мероприятие успешно добавлено!");
      router.push(`/events?tour_uuid=${uuid}`);
    } else {
      alert("Ошибка при добавлении мероприятия.");
    }
  };

  return (
      <div className="form-container">
        <h1 id="mini_label">Добавить мероприятие</h1>
        <form onSubmit={handleSubmit}>
          <label>
            Название:
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
            />
          </label>
          <label>
            Тип мероприятия:
            <select
                value={eventType}
                onChange={(e) => setEventType(e.target.value)}
                required
            >
              <option value="">Выберите тип</option>
              <option value="flight">Авиаперелет</option>
              <option value="transfer">Трансфер</option>
              <option value="hotel">Отель</option>
              <option value="entertainment">Развлечения</option>
            </select>
          </label>
          {eventType === "flight" && (
              <label>
                Номер рейса:
                <input
                    type="text"
                    value={flightNumber}
                    onChange={(e) => setFlightNumber(e.target.value)}
                    required
                />
              </label>
          )}
          <label>
            Дата и время начала:
            <input
                type="datetime-local"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
            />
          </label>
          <label>
            Дата и время окончания:
            <input
                type="datetime-local"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                required
            />
          </label>
          <label>
            Место:
            <input
                type="text"
                value={eventData}
                onChange={(e) => setEventData(e.target.value)}
                required
            />
          </label>
          <button type="submit">Отправить</button>
        </form>
      </div>
  );
}