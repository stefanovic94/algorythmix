package main

import (
	"asset_management/src/application/controllers/rest/assets"
	"asset_management/src/libs/logging"
	"context"
	"errors"
	"github.com/JGLTechnologies/gin-rate-limit"
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	log := logger.GetLogger()

	router := gin.Default()

	// Define here how many requests per second per IP
	store := ratelimit.InMemoryStore(&ratelimit.InMemoryOptions{
		Rate:  time.Second,
		Limit: 5,
	})
	rateLimitMiddleware := ratelimit.RateLimiter(store, &ratelimit.Options{
		ErrorHandler: func(c *gin.Context, info ratelimit.Info) {
			c.JSON(http.StatusTooManyRequests, gin.H{
				"status": "Rate limit exceeded",
			})
		},
		KeyFunc: func(c *gin.Context) string {
			return c.ClientIP()
		},
	})
	router.Use(rateLimitMiddleware)

	router.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
		})
	})

	assets.AssetRouter(router.Group("/assets"))

	srv := &http.Server{
		Addr:    ":8000",
		Handler: router.Handler(),
	}

	go func() {
		// service connections
		if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			log.Warn().Err(err)
		}
	}()

	// Wait for interrupt signal to gracefully shut down the server with
	// a timeout of n seconds.
	quit := make(chan os.Signal, 1)
	// kill (no param) default send syscall.SIGTERM
	// kill -2 is syscall.SIGINT
	// kill -9 is syscall. SIGKILL but can't be caught, so don't need add it
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Info().Msg("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Error().Err(err).Msg("Error happened while trying to shut down server")
	}

	// catching ctx.Done().
	select {
	case <-ctx.Done():
		// this is where to close connections
		log.Info().Msg("Closing connections...")
	}

	log.Info().Msg("Server exited")
}
