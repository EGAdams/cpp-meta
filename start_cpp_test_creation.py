#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio

import fire

from metagpt.roles import CppArchitect, CppEngineer, CppProductManager, ProjectManager, QaEngineer
from metagpt.software_company import SoftwareCompany


async def startup(idea: str, investment: float = 3.0, n_round: int = 5,
                  code_review: bool = False, run_tests: bool = False):
    
    # read in prompt from file
    idea = """ Create a C++ Google Unit Test for the following file: ``` cpp #include "Mode1Score.h"\nMode1Score::Mode1Score( IPlayer* player1, IPlayer* player2, IPinInterface* pinInterface, IGameState* gameState, IHistory* history ) :\n_player1( player1 ),\n_player2( player2 ),\n_gameState( gameState ),\n_history( history ),\n_Mode1TieBreaker( player1, player2, pinInterface, gameState, history ),\n_pointLeds( player1, player2, pinInterface ),\n_gameLeds( player1, player2, pinInterface ),\n_setLeds( player1, player2, pinInterface ),\n_mode1WinSequences( player1, player2, pinInterface, gameState ),\n_undo( player1, player2, pinInterface, gameState ) {}\nMode1Score::~Mode1Score() {}\nvoid Mode1Score::updateScore( IPlayer* currentPlayer ) {\n    IPlayer* otherPlayer = currentPlayer->getOpponent();\nif ( currentPlayer->getPoints() >= 3 ) {\nif ( currentPlayer->getPoints() == otherPlayer->getPoints()) {\ncurrentPlayer->setPoints( 3 );\notherPlayer->setPoints( 3 );\n} else if ( currentPlayer->getPoints() > 3 && ( currentPlayer->getPoints() - otherPlayer->getPoints()) > 1 ) {\ncurrentPlayer->setGames( currentPlayer->getGames() + 1);\n_undo.memory();\ncurrentPlayer->number() == 1 ? mode1P1Games() : mode1P2Games(); }\nif ( currentPlayer->getPoints() == 4 ) {\n// std::cout << "inside updateScore().  points == 4.  setting point flash to 1..." << std::endl;\n_gameState->setPointFlash( 1 );\n_gameState->setPreviousTime( GameTimer::gameMillis());\n_gameState->setToggle( 0 ); }}\n// std::cout << "inside updateScore().  updating points..." << std::endl;\n_pointLeds.updatePoints(); }  ``` """    
    
    """Run a startup. Be a boss."""
    company = SoftwareCompany()
    company.hire([CppProductManager(),
                  CppArchitect(),
                  ProjectManager(),
                  CppEngineer( n_borg=5, use_code_review=code_review )])
    if run_tests:
        # developing features: run tests on the spot and identify bugs (bug fixing capability comes soon!)
        company.hire([QaEngineer()])
    company.invest(investment)
    company.start_project(idea)
    await company.run(n_round=n_round)


def main(idea: str, investment: float = 3.0, n_round: int = 5, code_review: bool = False, run_tests: bool = False):
    """
    We are a software startup comprised of AI. By investing in us, you are empowering a future filled with limitless possibilities.
    :param idea: Your innovative idea, such as "Creating a snake game."
    :param investment: As an investor, you have the opportunity to contribute a certain dollar amount to this AI company.
    :param n_round:
    :param code_review: Whether to use code review.
    :return:
    """
    asyncio.run(startup(idea, investment, n_round, code_review, run_tests))


if __name__ == '__main__':
    fire.Fire(main)
