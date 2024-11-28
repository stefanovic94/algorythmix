from typing import Any, Literal

from pydantic import BaseModel, Field


class KafkaConfig(BaseModel):
    host: str = Field(...)
    security_protocol: Literal["SASL_SSL"] = Field("SASL_SSL")
    sasl_mechanism: Literal["PLAIN"] = Field("PLAIN")
    enable_cert_verification: bool = Field(False)
    username: str = Field(...)
    password: str = Field(...)
    client_id: str = Field(...)
    queue_buffering_max_messages: int = Field(10_000_000)
    compression_type: Literal["gzip"] = Field("gzip")
    linger: int = Field(1_000, description="In milliseconds")
    batch_size: int = Field(32_000, description="In bytes")  # 32 KB
    group_id: str = Field(...)
    session_timeout: int = Field(350_000, description="In milliseconds")
    max_poll_interval: int = Field(350_000, description="In milliseconds")
    auto_offset_reset: Literal["earliest"] = Field(
        "earliest",
        description="starts reading from the beginning of the topic if no committed offsets exist",
    )
    fetch_min_bytes: int = Field(10_000)  # 10 KB

    def get_producer_config(self) -> dict[str, Any]:
        return {
            "bootstrap.servers": self.host,
            "security.protocol": self.security_protocol,
            "sasl.mechanism": self.sasl_mechanism,
            "enable.ssl.certificate.verification": self.enable_cert_verification,
            "sasl.username": self.username,
            "sasl.password": self.password,
            "client.id": self.client_id,
            "queue.buffering.max.messages": self.queue_buffering_max_messages,
            "compression.type": self.compression_type,
            "linger.ms": self.linger,
            "batch.size": self.batch_size,
        }

    def get_consumer_config(self) -> dict[str, Any]:
        return {
            "bootstrap.servers": self.host,
            "security.protocol": self.security_protocol,
            "sasl.mechanism": self.sasl_mechanism,
            "enable.ssl.certificate.verification": self.enable_cert_verification,
            "sasl.username": self.username,
            "sasl.password": self.password,
            "client.id": self.client_id,
            "group.id": self.group_id,
            "session.timeout.ms": self.session_timeout,
            "max.poll.interval.ms": self.max_poll_interval,
            "auto.offset.reset": self.auto_offset_reset,
            "fetch.min.bytes": self.fetch_min_bytes,
        }
