from absl import app

from m300_toolbox.actions import ACTIONS


def app_run_main() -> None:
  app.run(main)


def main(_: list[str]) -> None:
  for action in ACTIONS:
    action._execute_and_print()


if __name__ == '__main__':
  app_run_main()
